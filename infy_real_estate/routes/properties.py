"""
INFY Real Estate - Property Routes
Property listing, search, details, comparison, and saved properties
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Property, City, State, PropertyImage, SavedProperty
from ai_modules.price_predictor import format_indian_price, predict_price, get_roi_analysis
from ai_modules.investment_scorer import calculate_investment_score
from ai_modules.trust_scorer import calculate_trust_score
from ai_modules.growth_predictor import predict_growth, get_neighborhood_intelligence, get_negotiation_advice

properties_bp = Blueprint('properties', __name__)


@properties_bp.route('/')
def listing():
    """Property listing with filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Build query with filters
    query = Property.query

    # Filter by city
    city_id = request.args.get('city_id', type=int)
    if city_id:
        query = query.filter_by(city_id=city_id)

    # Filter by state
    state_id = request.args.get('state_id', type=int)
    if state_id:
        city_ids = [c.id for c in City.query.filter_by(state_id=state_id).all()]
        if city_ids:
            query = query.filter(Property.city_id.in_(city_ids))

    # Filter by property type
    property_type = request.args.get('property_type')
    if property_type:
        query = query.filter_by(property_type=property_type)

    # Filter by price range
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)

    # Filter by bedrooms
    bedrooms = request.args.get('bedrooms', type=int)
    if bedrooms:
        query = query.filter(Property.bedrooms >= bedrooms)

    # Filter by bathrooms
    bathrooms = request.args.get('bathrooms', type=int)
    if bathrooms:
        query = query.filter(Property.bathrooms >= bathrooms)

    # Amenity filters
    if request.args.get('car_parking'):
        query = query.filter_by(car_parking=True)
    if request.args.get('swimming_pool'):
        query = query.filter_by(swimming_pool=True)
    if request.args.get('power_backup'):
        query = query.filter_by(power_backup=True)
    if request.args.get('lift'):
        query = query.filter_by(lift=True)
    if request.args.get('gym'):
        query = query.filter_by(gym=True)
    if request.args.get('club_house'):
        query = query.filter_by(club_house=True)
    if request.args.get('garden'):
        query = query.filter_by(garden=True)
    if request.args.get('security'):
        query = query.filter_by(security=True)
    if request.args.get('children_play_area'):
        query = query.filter_by(children_play_area=True)
    if request.args.get('water_facility'):
        query = query.filter_by(water_facility=True)
    if request.args.get('pet_friendly'):
        query = query.filter_by(pet_friendly=True)
    if request.args.get('near_school'):
        query = query.filter_by(near_school=True)
    if request.args.get('near_hospital'):
        query = query.filter_by(near_hospital=True)
    if request.args.get('metro_connectivity'):
        query = query.filter_by(metro_connectivity=True)

    # Filter by furnished status
    furnished = request.args.get('furnished')
    if furnished:
        query = query.filter_by(furnished=furnished)

    # Sorting
    sort_by = request.args.get('sort', 'newest')
    if sort_by == 'price_low':
        query = query.order_by(Property.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Property.price.desc())
    elif sort_by == 'area':
        query = query.order_by(Property.area_sqft.desc())
    else:
        query = query.order_by(Property.created_at.desc())

    # Paginate
    properties = query.paginate(page=page, per_page=per_page, error_out=False)

    # Get filter options
    states = State.query.order_by(State.name).all()
    cities = City.query.order_by(City.name).all()

    property_types = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Warehouse', 'Land', 'Plots', 'Luxury Villa',
                      'Gated Community House']

    return render_template('properties/listing.html',
                           properties=properties,
                           states=states,
                           cities=cities,
                           property_types=property_types,
                           format_price=format_indian_price)


@properties_bp.route('/<int:property_id>')
def detail(property_id):
    """Property detail page with AI insights"""
    property_obj = Property.query.get_or_404(property_id)
    images = PropertyImage.query.filter_by(property_id=property_id).all()

    # Get city name
    city = City.query.get(property_obj.city_id)
    city_name = city.name if city else 'Unknown'

    # Count amenities
    amenities_count = sum([
        property_obj.car_parking, property_obj.swimming_pool,
        property_obj.power_backup, property_obj.lift,
        property_obj.gym, property_obj.club_house,
        property_obj.garden, property_obj.security,
        property_obj.children_play_area, property_obj.water_facility,
        property_obj.pet_friendly, property_obj.near_school,
        property_obj.near_hospital, property_obj.metro_connectivity
    ])

    # AI Price Prediction
    prediction = predict_price(
        city=city_name,
        area_sqft=property_obj.area_sqft,
        property_type=property_obj.property_type,
        bedrooms=property_obj.bedrooms,
        bathrooms=property_obj.bathrooms,
        property_age=property_obj.property_age,
        amenities_count=amenities_count
    )

    # AI Investment Score
    investment = calculate_investment_score(
        city=city_name,
        property_type=property_obj.property_type,
        price=property_obj.price,
        area_sqft=property_obj.area_sqft,
        bedrooms=property_obj.bedrooms,
        amenities_count=amenities_count,
        property_age=property_obj.property_age,
        near_metro=property_obj.metro_connectivity
    )

    # AI Trust Score
    trust = calculate_trust_score({
        'price': property_obj.price,
        'area_sqft': property_obj.area_sqft,
        'city': city_name,
        'owner_name': property_obj.owner_name,
        'owner_phone': property_obj.owner_phone,
        'builder_name': property_obj.builder_name,
        'description': property_obj.description,
        'address': property_obj.address,
        'pincode': property_obj.pincode,
        'image_count': len(images),
        'is_verified': property_obj.is_verified,
    })

    # AI Growth Prediction
    growth = predict_growth(city_name, property_obj.locality)

    # ROI Analysis
    roi = get_roi_analysis(property_obj.price, city_name,
                           property_obj.property_type, property_obj.area_sqft)

    # Neighborhood Intelligence
    neighborhood = get_neighborhood_intelligence(city_name, property_obj.locality)

    # Negotiation Advice
    negotiation = get_negotiation_advice(
        property_obj.price, city_name, property_obj.area_sqft,
        property_obj.property_type, property_obj.property_age
    )

    # Related properties (same city, similar type)
    related = Property.query.filter(
        Property.city_id == property_obj.city_id,
        Property.id != property_obj.id,
        Property.property_type == property_obj.property_type
    ).limit(4).all()

    if len(related) < 4:
        more = Property.query.filter(
            Property.city_id == property_obj.city_id,
            Property.id != property_obj.id,
            Property.id.notin_([r.id for r in related])
        ).limit(4 - len(related)).all()
        related.extend(more)

    # Check if saved by current user
    is_saved = False
    if current_user.is_authenticated:
        is_saved = SavedProperty.query.filter_by(
            user_id=current_user.id, property_id=property_id).first() is not None

    return render_template('properties/detail.html',
                           property=property_obj,
                           images=images,
                           city_name=city_name,
                           prediction=prediction,
                           investment=investment,
                           trust=trust,
                           growth=growth,
                           roi=roi,
                           neighborhood=neighborhood,
                           negotiation=negotiation,
                           related=related,
                           is_saved=is_saved,
                           format_price=format_indian_price)


@properties_bp.route('/save/<int:property_id>', methods=['POST'])
@login_required
def save_property(property_id):
    """Save/unsave a property"""
    existing = SavedProperty.query.filter_by(
        user_id=current_user.id, property_id=property_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash('Property removed from saved list.', 'info')
    else:
        saved = SavedProperty(user_id=current_user.id, property_id=property_id)
        db.session.add(saved)
        db.session.commit()
        flash('Property saved successfully!', 'success')

    return redirect(url_for('properties.detail', property_id=property_id))


@properties_bp.route('/compare')
def compare():
    """Compare up to 5 properties"""
    property_ids = request.args.getlist('ids', type=int)
    if not property_ids:
        flash('Select properties to compare.', 'info')
        return redirect(url_for('properties.listing'))

    properties_list = Property.query.filter(Property.id.in_(property_ids[:5])).all()
    comparisons = []

    for prop in properties_list:
        city = City.query.get(prop.city_id)
        city_name = city.name if city else 'Unknown'
        amenities_count = sum([
            prop.car_parking, prop.swimming_pool, prop.power_backup,
            prop.lift, prop.gym, prop.club_house, prop.garden,
            prop.security, prop.children_play_area, prop.water_facility
        ])

        investment = calculate_investment_score(
            city=city_name, property_type=prop.property_type,
            price=prop.price, area_sqft=prop.area_sqft,
            bedrooms=prop.bedrooms, amenities_count=amenities_count,
            property_age=prop.property_age, near_metro=prop.metro_connectivity
        )

        roi = get_roi_analysis(prop.price, city_name, prop.property_type, prop.area_sqft)

        comparisons.append({
            'property': prop,
            'city_name': city_name,
            'investment': investment,
            'roi': roi,
            'price_per_sqft': round(prop.price / prop.area_sqft) if prop.area_sqft else 0,
        })

    return render_template('properties/compare.html',
                           comparisons=comparisons,
                           format_price=format_indian_price)


@properties_bp.route('/search')
def smart_search():
    """Smart property search page"""
    states = State.query.order_by(State.name).all()
    property_types = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Warehouse', 'Land', 'Plots', 'Luxury Villa',
                      'Gated Community House']
    return render_template('properties/search.html',
                           states=states,
                           property_types=property_types)
