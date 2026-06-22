"""
INFY Nest Real Estate - AI Chatbot (INFY AI)
Conversational AI assistant for real estate queries
"""
import random
import re


# Knowledge base for real estate topics
KNOWLEDGE_BASE = {
    'home_loan': {
        'keywords': ['loan', 'emi', 'interest', 'bank', 'finance', 'mortgage', 'home loan'],
        'responses': [
            "Here's what you need to know about home loans:\n\n"
            "**Current Interest Rates (2024-25):**\n"
            "- SBI: 8.40% - 9.65%\n"
            "- HDFC: 8.35% - 9.50%\n"
            "- ICICI: 8.40% - 9.45%\n"
            "- Axis: 8.55% - 9.60%\n\n"
            "**Eligibility:**\n"
            "- Age: 21-65 years\n"
            "- Min Income: Rs 25,000/month\n"
            "- CIBIL Score: 700+\n\n"
            "**Documents Required:**\n"
            "- PAN Card, Aadhar Card\n"
            "- Salary slips (last 3 months)\n"
            "- Bank statements (last 6 months)\n"
            "- Property documents\n\n"
            "Would you like me to calculate your EMI or help with anything else?",
        ]
    },
    'registration': {
        'keywords': ['registration', 'stamp duty', 'registry', 'document', 'legal'],
        'responses': [
            "**Property Registration Process in India:**\n\n"
            "**Step 1:** Verify property documents (Title deed, Encumbrance certificate)\n\n"
            "**Step 2:** Pay Stamp Duty\n"
            "- Maharashtra: 5-6%\n"
            "- Karnataka: 5%\n"
            "- Telangana: 4%\n"
            "- Tamil Nadu: 7%\n"
            "- Delhi: 4-6%\n\n"
            "**Step 3:** Registration fee (usually 1% of property value)\n\n"
            "**Step 4:** Execute Sale Deed at Sub-Registrar office\n\n"
            "**Step 5:** Get mutation done at Municipal Corporation\n\n"
            "**Documents Required:**\n"
            "- Sale Agreement\n"
            "- ID Proof of both parties\n"
            "- Property tax receipts\n"
            "- NOC from society/builder\n\n"
            "Need help with anything specific?",
        ]
    },
    'investment': {
        'keywords': ['invest', 'investment', 'returns', 'profit', 'appreciation', 'roi'],
        'responses': [
            "**Top Investment Locations in India (2024-25):**\n\n"
            "**Tier 1 Cities:**\n"
            "1. Hyderabad - Growth: 12-15% annually\n"
            "2. Bengaluru - Growth: 10-14% annually\n"
            "3. Pune - Growth: 10-13% annually\n"
            "4. Mumbai (Navi Mumbai) - Growth: 9-12% annually\n\n"
            "**Tier 2 Cities (High Growth):**\n"
            "1. Indore - Growth: 15-20% annually\n"
            "2. Ahmedabad - Growth: 12-16% annually\n"
            "3. Lucknow - Growth: 13-17% annually\n\n"
            "**Investment Tips:**\n"
            "- Buy near upcoming metro stations\n"
            "- Look for IT corridor developments\n"
            "- Check for upcoming infrastructure projects\n"
            "- Consider rental yield (aim for 3-4%)\n\n"
            "Want me to analyze a specific location or property?",
        ]
    },
    'vastu': {
        'keywords': ['vastu', 'direction', 'facing', 'north', 'south', 'east', 'west'],
        'responses': [
            "**Vastu Tips for Property Buyers:**\n\n"
            "**Best Facing Directions:**\n"
            "- North-East: Most auspicious\n"
            "- East: Good for health and prosperity\n"
            "- North: Good for career and finances\n\n"
            "**Key Vastu Points:**\n"
            "- Main entrance: North or East preferred\n"
            "- Kitchen: South-East corner\n"
            "- Master Bedroom: South-West\n"
            "- Bathroom: North-West\n"
            "- Living Room: North-East\n\n"
            "**Avoid:**\n"
            "- T-junction facing properties\n"
            "- Properties near temples/graveyards\n"
            "- Irregular shaped plots\n\n"
            "Would you like property recommendations based on Vastu?",
        ]
    },
    'tax': {
        'keywords': ['tax', 'gst', 'income tax', 'capital gains', 'section 80'],
        'responses': [
            "**Property Tax Benefits in India:**\n\n"
            "**Under Construction Property:**\n"
            "- GST: 5% (without ITC) for non-affordable\n"
            "- GST: 1% for affordable housing (<45 lakhs)\n\n"
            "**Income Tax Benefits:**\n"
            "- Section 80C: Up to ₹1.5 lakh on principal repayment\n"
            "- Section 24(b): Up to ₹2 lakh on interest (self-occupied)\n"
            "- Section 80EEA: Additional ₹1.5 lakh for first-time buyers\n\n"
            "**Capital Gains Tax:**\n"
            "- Short-term (< 2 years): As per income slab\n"
            "- Long-term (> 2 years): 20% with indexation\n"
            "- Section 54: Exempt if reinvested in property\n\n"
            "Need more details on any specific tax topic?",
        ]
    },
    'rent': {
        'keywords': ['rent', 'rental', 'tenant', 'lease', 'rental agreement'],
        'responses': [
            "**Rental Guide for India:**\n\n"
            "**Average Rental Yields by City:**\n"
            "- Bengaluru: 3.5-4.5%\n"
            "- Mumbai: 2.5-3.5%\n"
            "- Hyderabad: 3.5-4.5%\n"
            "- Pune: 3-4%\n"
            "- Chennai: 3-3.8%\n\n"
            "**Rental Agreement Essentials:**\n"
            "- Standard duration: 11 months\n"
            "- Security deposit: 2-10 months rent\n"
            "- Registration required if > 11 months\n"
            "- Notice period: Usually 1-2 months\n\n"
            "**For Landlords:**\n"
            "- Screen tenants thoroughly\n"
            "- Get police verification done\n"
            "- Include maintenance clauses\n"
            "- Keep property well-maintained\n\n"
            "Want help finding rental properties?",
        ]
    }
}

# Property search patterns
PROPERTY_PATTERNS = [
    r'(?:need|want|looking for|find|search|show)\s+(?:a\s+)?(\w+)\s+(?:in|at|near)\s+(\w+)',
    r'(\w+)\s+(?:in|at|near)\s+(\w+)\s+(?:under|below|within)\s+(\d+)',
    r'(?:budget|price)\s+(?:is|of)?\s*(?:under|below|within)?\s*(\d+)',
]


def generate_response(user_message, properties=None):
    """
    Generate AI response for user query.
    Uses keyword matching and pattern recognition.
    """
    message_lower = user_message.lower().strip()

    # Check for greetings
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good evening', 'namaste']
    if any(g in message_lower for g in greetings):
        return (
            "Hello! Welcome to INFY AI - your intelligent real estate assistant! 🏠\n\n"
            "I can help you with:\n"
            "- 🔍 Finding properties (e.g., 'Show me villas in Hyderabad under 1 crore')\n"
            "- 💰 Investment advice\n"
            "- 🏦 Home loan information\n"
            "- 📋 Property registration process\n"
            "- 📊 Price predictions\n"
            "- 🧮 EMI calculations\n"
            "- 🏡 Vastu tips\n\n"
            "How can I help you today?"
        )

    # Check for thanks
    thanks = ['thank', 'thanks', 'thankyou', 'thank you', 'great', 'awesome', 'helpful']
    if any(t in message_lower for t in thanks):
        return (
            "You're welcome! Happy to help! 😊\n\n"
            "Feel free to ask me anything else about:\n"
            "- Property search\n"
            "- Price predictions\n"
            "- Investment analysis\n"
            "- Home loans & EMI\n\n"
            "I'm here 24/7 to assist you!"
        )

    # Check knowledge base topics
    # BUT only if no properties were found from the database
    # (if properties exist, user is searching for specific city/type results)
    if not properties:
        for topic, data in KNOWLEDGE_BASE.items():
            if any(kw in message_lower for kw in data['keywords']):
                return random.choice(data['responses'])

    # Check for EMI calculation
    if 'emi' in message_lower or ('calculate' in message_lower and not properties):
        return calculate_emi_response(message_lower)

    # Check for property search
    if properties or any(word in message_lower for word in ['villa', 'apartment', 'flat', 'house', 'property', 'bhk',
                                               'show', 'find', 'search', 'looking', 'need', 'want',
                                               'properties', 'listing', 'available']):
        return generate_property_search_response(message_lower, properties)

    # Check for price query
    if any(word in message_lower for word in ['price', 'cost', 'worth', 'value', 'rate']):
        return (
            "I can help you with property prices! 📊\n\n"
            "To give you accurate price estimates, please tell me:\n"
            "1. **City/Location** you're interested in\n"
            "2. **Property type** (Apartment/Villa/House)\n"
            "3. **Area** in sq ft\n"
            "4. **Number of bedrooms**\n\n"
            "Or you can use our **AI Price Predictor** tool for detailed forecasts "
            "with 1-year, 3-year, and 5-year predictions!\n\n"
            "Example: 'What's the price of a 3BHK apartment in Hyderabad, 1500 sq ft?'"
        )

    # Check for comparison
    if 'compare' in message_lower or 'vs' in message_lower or 'versus' in message_lower:
        return (
            "I can help you compare properties! 🔄\n\n"
            "You can compare up to 5 properties on our platform. "
            "The comparison includes:\n"
            "- Price per sq ft\n"
            "- Investment Score\n"
            "- ROI potential\n"
            "- Location Score\n"
            "- Amenities\n"
            "- AI Recommendation\n\n"
            "To compare, save properties to your favorites and use the Compare feature, "
            "or tell me which properties/locations you'd like to compare!"
        )

    # Default helpful response
    return (
        "I'd be happy to help you with that! Here's what I can assist with:\n\n"
        "**Property Search:**\n"
        "- Tell me your city, budget, and preferences\n"
        "- Example: 'Find 3BHK apartments in Bengaluru under 80 lakhs'\n\n"
        "**AI Tools:**\n"
        "- Price Prediction\n"
        "- Investment Analysis\n"
        "- ROI Calculator\n"
        "- Neighborhood Intelligence\n\n"
        "**Knowledge:**\n"
        "- Home Loans & EMI\n"
        "- Registration Process\n"
        "- Tax Benefits\n"
        "- Vastu Tips\n\n"
        "Please ask a specific question and I'll provide detailed guidance!"
    )


def calculate_emi_response(message):
    """Generate EMI calculation response"""
    # Try to extract amount
    numbers = re.findall(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac|crore|cr)?', message)

    if numbers:
        amount = float(numbers[0])
        if 'crore' in message or 'cr' in message:
            amount *= 10000000
        elif 'lakh' in message or 'lac' in message:
            amount *= 100000
        elif amount < 1000:
            amount *= 100000  # Assume lakhs

        # Calculate EMI for common tenures
        rate = 8.5 / 12 / 100  # 8.5% annual
        emi_20 = amount * rate * (1 + rate) ** 240 / ((1 + rate) ** 240 - 1)
        emi_15 = amount * rate * (1 + rate) ** 180 / ((1 + rate) ** 180 - 1)
        emi_10 = amount * rate * (1 + rate) ** 120 / ((1 + rate) ** 120 - 1)

        from ai_modules.price_predictor import format_indian_price
        return (
            f"**EMI Calculation for Loan Amount: {format_indian_price(amount)}**\n\n"
            f"(At 8.5% interest rate)\n\n"
            f"| Tenure | Monthly EMI | Total Interest | Total Payment |\n"
            f"|--------|------------|----------------|---------------|\n"
            f"| 10 Years | {format_indian_price(emi_10)} | {format_indian_price(emi_10*120 - amount)} | {format_indian_price(emi_10*120)} |\n"
            f"| 15 Years | {format_indian_price(emi_15)} | {format_indian_price(emi_15*180 - amount)} | {format_indian_price(emi_15*180)} |\n"
            f"| 20 Years | {format_indian_price(emi_20)} | {format_indian_price(emi_20*240 - amount)} | {format_indian_price(emi_20*240)} |\n\n"
            f"**Tips to reduce EMI:**\n"
            f"- Make a higher down payment (20-30%)\n"
            f"- Choose shorter tenure\n"
            f"- Maintain CIBIL score above 750\n"
            f"- Compare rates from multiple banks\n\n"
            f"Need help with anything else?"
        )

    return (
        "**EMI Calculator:**\n\n"
        "To calculate your EMI, please provide:\n"
        "- Loan amount (e.g., '50 lakhs' or '1 crore')\n"
        "- Or just tell me the property price and I'll estimate!\n\n"
        "Example: 'Calculate EMI for 60 lakhs home loan'\n\n"
        "Quick reference at 8.5% interest:\n"
        "- ₹30L for 20 years = ~₹26,000/month\n"
        "- ₹50L for 20 years = ~₹43,000/month\n"
        "- ₹75L for 20 years = ~₹65,000/month\n"
        "- ₹1Cr for 20 years = ~₹87,000/month"
    )


def generate_property_search_response(message, properties=None):
    """Generate response for property search queries"""
    # Extract city names
    cities = ['hyderabad', 'bengaluru', 'bangalore', 'mumbai', 'delhi', 'pune',
              'chennai', 'kolkata', 'ahmedabad', 'jaipur', 'noida', 'gurgaon',
              'chandigarh', 'lucknow', 'indore', 'kochi', 'cochin', 'vizag',
              'coimbatore', 'madurai', 'surat', 'nagpur', 'thane', 'bhopal']
    found_city = None
    for city in cities:
        if city in message:
            found_city = city.title()
            if found_city == 'Bangalore':
                found_city = 'Bengaluru'
            elif found_city == 'Cochin':
                found_city = 'Kochi'
            break

    # Extract property type
    types = {'villa': 'Villa', 'apartment': 'Apartment', 'flat': 'Apartment',
             'house': 'Independent House', 'penthouse': 'Penthouse',
             'studio': 'Studio Apartment', 'farm': 'Farm House'}
    found_type = None
    for key, val in types.items():
        if key in message:
            found_type = val
            break

    response = f"Based on your search"
    if found_city:
        response += f" in **{found_city}**"
    if found_type:
        response += f" for **{found_type}**"
    response += ":\n\n"

    if properties:
        response += "Here are some matching properties:\n\n"
        for i, prop in enumerate(properties[:5], 1):
            from ai_modules.price_predictor import format_indian_price
            response += f"**{i}. {prop.title}**\n"
            response += f"   - Price: {format_indian_price(prop.price)}\n"
            response += f"   - Area: {prop.area_sqft} sq ft | {prop.bedrooms} BHK\n"
            response += f"   - Location: {prop.locality}"
            if prop.city:
                response += f", {prop.city.name}"
            response += "\n\n"
        response += "\nWould you like more details on any of these properties?"
    else:
        response += (
            "I'd recommend checking our property listings with these filters. "
            "You can also use our **Smart Search** feature to find exactly what you need!\n\n"
            "**Tips for your search:**\n"
            f"- {'Explore localities in ' + found_city + ' for better value' if found_city else 'Specify a city for targeted results'}\n"
            "- Use our AI Price Predictor to know fair prices\n"
            "- Check Investment Score before buying\n"
            "- Compare properties side by side\n\n"
            "Would you like me to help narrow down your search?"
        )

    return response
