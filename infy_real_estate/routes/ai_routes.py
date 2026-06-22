"""
INFY Nest Real Estate - AI Routes
Price Prediction, Chatbot, Investment Analysis
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import (Property, City, State, ChatSession, ChatMessage,
                    PredictionHistory)
from ai_modules.price_predictor import predict_price, format_indian_price, get_roi_analysis
from ai_modules.investment_scorer import calculate_investment_score
from ai_modules.growth_predictor import predict_growth, get_neighborhood_intelligence
from ai_modules.chatbot import generate_response

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/price-predictor', methods=['GET', 'POST'])
def price_predictor():
    """AI Price Prediction page"""
    states = State.query.order_by(State.name).all()
    prediction = None

    if request.method == 'POST':
        city_name = request.form.get('city', '')
        area_sqft = float(request.form.get('area_sqft', 1000))
        property_type = request.form.get('property_type', 'Apartment')
        bedrooms = int(request.form.get('bedrooms', 2))
        bathrooms = int(request.form.get('bathrooms', 2))
        property_age = int(request.form.get('property_age', 0))
        amenities = int(request.form.get('amenities', 5))

        prediction = predict_price(
            city=city_name,
            area_sqft=area_sqft,
            property_type=property_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            property_age=property_age,
            amenities_count=amenities
        )

        # Format prices for display
        prediction['current_price_fmt'] = format_indian_price(prediction['current_price'])
        prediction['price_1year_fmt'] = format_indian_price(prediction['price_1year'])
        prediction['price_3year_fmt'] = format_indian_price(prediction['price_3year'])
        prediction['price_5year_fmt'] = format_indian_price(prediction['price_5year'])

        # Save to history if logged in
        if current_user.is_authenticated:
            history = PredictionHistory(
                user_id=current_user.id,
                city=city_name,
                area_sqft=area_sqft,
                property_type=property_type,
                bedrooms=bedrooms,
                current_price=prediction['current_price'],
                price_1year=prediction['price_1year'],
                price_3year=prediction['price_3year'],
                price_5year=prediction['price_5year'],
                confidence=prediction['confidence']
            )
            db.session.add(history)
            db.session.commit()

    property_types = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Warehouse', 'Land', 'Plots', 'Luxury Villa',
                      'Gated Community House']

    return render_template('ai/price_predictor.html',
                           states=states,
                           property_types=property_types,
                           prediction=prediction)


@ai_bp.route('/investment-analyzer', methods=['GET', 'POST'])
def investment_analyzer():
    """AI Investment Analysis page"""
    states = State.query.order_by(State.name).all()
    result = None

    if request.method == 'POST':
        city_name = request.form.get('city', '')
        property_type = request.form.get('property_type', 'Apartment')
        price = float(request.form.get('price', 5000000))
        area_sqft = float(request.form.get('area_sqft', 1000))
        bedrooms = int(request.form.get('bedrooms', 2))
        amenities = int(request.form.get('amenities', 5))
        property_age = int(request.form.get('property_age', 0))
        near_metro = request.form.get('near_metro') == 'yes'

        investment = calculate_investment_score(
            city=city_name,
            property_type=property_type,
            price=price,
            area_sqft=area_sqft,
            bedrooms=bedrooms,
            amenities_count=amenities,
            property_age=property_age,
            near_metro=near_metro
        )

        roi = get_roi_analysis(price, city_name, property_type, area_sqft)
        growth = predict_growth(city_name)
        neighborhood = get_neighborhood_intelligence(city_name)

        result = {
            'investment': investment,
            'roi': roi,
            'growth': growth,
            'neighborhood': neighborhood,
            'city': city_name,
            'price_fmt': format_indian_price(price),
        }

    property_types = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Land', 'Plots', 'Luxury Villa',
                      'Gated Community House']

    return render_template('ai/investment_analyzer.html',
                           states=states,
                           property_types=property_types,
                           result=result,
                           format_price=format_indian_price)


@ai_bp.route('/chatbot')
@login_required
def chatbot():
    """AI Chatbot page"""
    sessions = ChatSession.query.filter_by(user_id=current_user.id)\
        .order_by(ChatSession.created_at.desc()).all()
    return render_template('ai/chatbot.html', sessions=sessions)


@ai_bp.route('/chatbot/new', methods=['POST'])
@login_required
def new_chat():
    """Create new chat session"""
    session = ChatSession(user_id=current_user.id, title='New Chat')
    db.session.add(session)
    db.session.commit()
    return jsonify({'session_id': session.id})


@ai_bp.route('/chatbot/message', methods=['POST'])
@login_required
def chat_message():
    """Send message and get AI response"""
    data = request.get_json()
    session_id = data.get('session_id')
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Empty message'}), 400

    # Get or create session
    chat_session = None
    if session_id:
        chat_session = ChatSession.query.get(session_id)

    if not chat_session:
        chat_session = ChatSession(user_id=current_user.id, title=message[:50])
        db.session.add(chat_session)
        db.session.commit()

    # Save user message
    user_msg = ChatMessage(session_id=chat_session.id, role='user', content=message)
    db.session.add(user_msg)

    # Generate AI response
    # Try to find matching properties based on user's message
    properties = _find_matching_properties(message)
    ai_response = generate_response(message, properties)

    # Save AI response
    ai_msg = ChatMessage(session_id=chat_session.id, role='assistant', content=ai_response)
    db.session.add(ai_msg)

    # Update session title from first message
    if ChatMessage.query.filter_by(session_id=chat_session.id, role='user').count() == 1:
        chat_session.title = message[:50]

    db.session.commit()

    return jsonify({
        'session_id': chat_session.id,
        'response': ai_response,
        'session_title': chat_session.title
    })


@ai_bp.route('/chatbot/history/<int:session_id>')
@login_required
def chat_history(session_id):
    """Get chat history for a session"""
    chat_session = ChatSession.query.get_or_404(session_id)
    if chat_session.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    messages = [{
        'role': msg.role,
        'content': msg.content,
        'time': msg.created_at.strftime('%I:%M %p')
    } for msg in chat_session.messages]

    return jsonify({'messages': messages, 'title': chat_session.title})


@ai_bp.route('/chatbot/delete/<int:session_id>', methods=['POST'])
@login_required
def delete_chat(session_id):
    """Delete a chat session"""
    chat_session = ChatSession.query.get_or_404(session_id)
    if chat_session.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    ChatMessage.query.filter_by(session_id=session_id).delete()
    db.session.delete(chat_session)
    db.session.commit()

    return jsonify({'success': True})



def _find_matching_properties(message):
    """
    Extract city, budget, and property type from user message
    and return matching properties from the database.
    """
    import re
    message_lower = message.lower().strip()

    # Comprehensive city aliases and common misspellings
    city_aliases = {
        # Bengaluru variants
        'bengaluru': 'Bengaluru', 'bangalore': 'Bengaluru', 'banglore': 'Bengaluru',
        'bengluru': 'Bengaluru', 'benglore': 'Bengaluru', 'bangaluru': 'Bengaluru',
        'bangluru': 'Bengaluru', 'blr': 'Bengaluru',
        # Mumbai variants
        'mumbai': 'Mumbai', 'bombay': 'Mumbai', 'mombai': 'Mumbai',
        # Chennai variants
        'chennai': 'Chennai', 'madras': 'Chennai', 'chenai': 'Chennai',
        # Hyderabad variants
        'hyderabad': 'Hyderabad', 'hyd': 'Hyderabad', 'hydrabad': 'Hyderabad',
        # Kolkata variants
        'kolkata': 'Kolkata', 'calcutta': 'Kolkata', 'kolkatta': 'Kolkata',
        # Delhi variants
        'delhi': 'New Delhi', 'new delhi': 'New Delhi', 'dilli': 'New Delhi',
        # Pune variants
        'pune': 'Pune', 'poona': 'Pune',
        # Gurgaon variants
        'gurgaon': 'Gurgaon', 'gurugram': 'Gurgaon', 'gurgoan': 'Gurgaon',
        # Noida
        'noida': 'Noida', 'greater noida': 'Noida',
        # Others
        'ahmedabad': 'Ahmedabad', 'amdavad': 'Ahmedabad',
        'jaipur': 'Jaipur', 'jaypur': 'Jaipur',
        'lucknow': 'Lucknow', 'lakhnau': 'Lucknow',
        'chandigarh': 'Chandigarh',
        'kochi': 'Kochi', 'cochin': 'Kochi',
        'indore': 'Indore',
        'coimbatore': 'Coimbatore',
        'visakhapatnam': 'Visakhapatnam', 'vizag': 'Visakhapatnam',
        'mysuru': 'Mysuru', 'mysore': 'Mysuru',
        'mangaluru': 'Mangaluru', 'mangalore': 'Mangaluru',
        'thiruvananthapuram': 'Thiruvananthapuram', 'trivandrum': 'Thiruvananthapuram',
        'bhubaneswar': 'Bhubaneswar',
        'patna': 'Patna',
        'ranchi': 'Ranchi',
        'guwahati': 'Guwahati',
        'dehradun': 'Dehradun',
        'surat': 'Surat',
        'nagpur': 'Nagpur',
        'nashik': 'Nashik',
        'vadodara': 'Vadodara', 'baroda': 'Vadodara',
        'thane': 'Thane',
        'bhopal': 'Bhopal',
    }

    # Step 1: Try alias matching first (handles misspellings)
    found_city = None
    for alias, actual_name in city_aliases.items():
        if alias in message_lower:
            found_city = City.query.filter(City.name.ilike(actual_name)).first()
            if found_city:
                break

    # Step 2: If no alias match, try matching against database city names
    if not found_city:
        all_cities = City.query.all()
        for city in all_cities:
            if city.name.lower() in message_lower:
                found_city = city
                break

    # Step 3: Fuzzy partial match - check if any word in message starts with a city name
    if not found_city:
        words = message_lower.split()
        all_cities = City.query.all()
        for city in all_cities:
            city_lower = city.name.lower()
            for word in words:
                # Check if word is at least 5 chars and closely matches a city name
                if len(word) >= 5 and len(city_lower) >= 5:
                    if city_lower.startswith(word[:5]) or word.startswith(city_lower[:5]):
                        found_city = city
                        break
            if found_city:
                break

    # Build query
    query = Property.query

    if found_city:
        query = query.filter_by(city_id=found_city.id)

    # Try to extract budget
    budget_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:cr|crore|crores)', message_lower)
    if budget_match:
        max_price = float(budget_match.group(1)) * 10000000
        query = query.filter(Property.price <= max_price)
    else:
        budget_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac|lakhs)', message_lower)
        if budget_match:
            max_price = float(budget_match.group(1)) * 100000
            query = query.filter(Property.price <= max_price)

    # Try to extract property type
    type_keywords = {
        'villa': 'Villa', 'apartment': 'Apartment', 'flat': 'Apartment',
        'house': 'Independent House', 'penthouse': 'Penthouse',
        'studio': 'Studio Apartment', 'farm': 'Farm House',
        'office': 'Commercial Office', 'shop': 'Shop',
        'land': 'Land', 'plot': 'Plots',
    }
    for keyword, ptype in type_keywords.items():
        if keyword in message_lower:
            query = query.filter_by(property_type=ptype)
            break

    # Try to extract bedrooms
    bhk_match = re.search(r'(\d+)\s*bhk', message_lower)
    if bhk_match:
        query = query.filter_by(bedrooms=int(bhk_match.group(1)))

    # Return matching properties (limit 10)
    properties = query.limit(10).all()

    # If no results with all filters, try just city
    if not properties and found_city:
        properties = Property.query.filter_by(city_id=found_city.id).limit(10).all()

    return properties
