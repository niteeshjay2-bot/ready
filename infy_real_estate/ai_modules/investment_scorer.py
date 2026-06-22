"""
INFY Nest Real Estate - AI Investment Score Calculator
Generates investment score from 0-100 based on multiple factors
"""
import random


# Location scores by city
LOCATION_SCORES = {
    'Mumbai': 92, 'Delhi': 88, 'Bengaluru': 95, 'Hyderabad': 93,
    'Chennai': 85, 'Pune': 90, 'Kolkata': 78, 'Ahmedabad': 82,
    'Jaipur': 75, 'Lucknow': 72, 'Chandigarh': 80, 'Gurgaon': 91,
    'Noida': 85, 'Ghaziabad': 72, 'Thane': 83, 'Navi Mumbai': 86,
    'Visakhapatnam': 74, 'Vijayawada': 70, 'Tirupati': 65,
    'Kakinada': 60, 'Guntur': 62, 'Warangal': 68, 'Karimnagar': 63,
    'Coimbatore': 78, 'Madurai': 68, 'Mysuru': 73, 'Mangaluru': 72,
    'Kochi': 80, 'Thiruvananthapuram': 75, 'Indore': 76,
    'Bhopal': 72, 'Nagpur': 74, 'Nashik': 71, 'Surat': 79,
    'Vadodara': 73, 'Rajkot': 68, 'Patna': 65, 'Ranchi': 62,
    'Bhubaneswar': 73, 'Guwahati': 70, 'Dehradun': 74,
}

# Infrastructure development factors
INFRASTRUCTURE_SCORES = {
    'Mumbai': 90, 'Delhi': 88, 'Bengaluru': 92, 'Hyderabad': 94,
    'Chennai': 83, 'Pune': 87, 'Gurgaon': 90, 'Noida': 86,
}


def calculate_investment_score(city, property_type, price, area_sqft, bedrooms,
                                amenities_count=0, property_age=0, near_metro=False):
    """
    Calculate AI Investment Score (0-100) based on multiple factors.
    """
    # 1. Location Score (30% weight)
    location_score = LOCATION_SCORES.get(city, 65)

    # 2. Price Value Score (20% weight) - lower price per sqft = better value
    price_per_sqft = price / area_sqft if area_sqft > 0 else 0
    if price_per_sqft < 3000:
        value_score = 95
    elif price_per_sqft < 5000:
        value_score = 85
    elif price_per_sqft < 8000:
        value_score = 75
    elif price_per_sqft < 12000:
        value_score = 65
    elif price_per_sqft < 18000:
        value_score = 55
    else:
        value_score = 45

    # 3. Amenities Score (15% weight)
    amenity_score = min(100, 50 + amenities_count * 5)

    # 4. Property Age Score (10% weight)
    if property_age <= 2:
        age_score = 95
    elif property_age <= 5:
        age_score = 85
    elif property_age <= 10:
        age_score = 70
    elif property_age <= 20:
        age_score = 55
    else:
        age_score = 40

    # 5. Infrastructure Score (15% weight)
    infra_score = INFRASTRUCTURE_SCORES.get(city, 65)
    if near_metro:
        infra_score = min(100, infra_score + 10)

    # 6. Rental Demand Score (10% weight)
    rental_cities = {'Bengaluru': 95, 'Mumbai': 90, 'Hyderabad': 92, 'Pune': 88,
                     'Gurgaon': 87, 'Chennai': 82, 'Delhi': 80, 'Noida': 83}
    rental_score = rental_cities.get(city, 65)

    # Calculate weighted score
    total_score = (
        location_score * 0.30 +
        value_score * 0.20 +
        amenity_score * 0.15 +
        age_score * 0.10 +
        infra_score * 0.15 +
        rental_score * 0.10
    )

    # Add small variance
    total_score += random.uniform(-2, 2)
    total_score = max(30, min(98, total_score))

    # Determine risk level
    if total_score >= 80:
        risk = 'Low'
        roi_label = 'High'
    elif total_score >= 60:
        risk = 'Medium'
        roi_label = 'Moderate'
    else:
        risk = 'High'
        roi_label = 'Low'

    # Investment recommendation
    if total_score >= 85:
        recommendation = 'Highly Recommended - Excellent Investment'
    elif total_score >= 75:
        recommendation = 'Recommended - Good Investment'
    elif total_score >= 60:
        recommendation = 'Moderate - Consider Other Options'
    else:
        recommendation = 'Not Recommended - High Risk'

    return {
        'investment_score': round(total_score, 1),
        'risk_level': risk,
        'roi_potential': roi_label,
        'recommendation': recommendation,
        'breakdown': {
            'location': round(location_score, 1),
            'value': round(value_score, 1),
            'amenities': round(amenity_score, 1),
            'age': round(age_score, 1),
            'infrastructure': round(infra_score, 1),
            'rental_demand': round(rental_score, 1),
        }
    }
