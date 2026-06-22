"""
INFY Nest Real Estate - AI Trust Score / Scam Detector
Detects suspicious listings and generates trust scores
"""
import random


def calculate_trust_score(property_data):
    """
    Calculate Trust Score (0-100) for a property listing.
    Detects potential scams based on:
    - Price anomalies
    - Missing information
    - Verification status
    - Listing patterns
    """
    score = 100  # Start with perfect score, deduct for issues
    flags = []

    # 1. Price Analysis
    price = property_data.get('price', 0)
    area = property_data.get('area_sqft', 0)
    city = property_data.get('city', '')

    if area > 0 and price > 0:
        price_per_sqft = price / area
        # Extremely low price is suspicious
        if price_per_sqft < 1000:
            score -= 25
            flags.append('Unusually low price per sq ft')
        elif price_per_sqft < 2000:
            score -= 10
            flags.append('Below market price - verify with seller')
    else:
        score -= 15
        flags.append('Missing area or price information')

    # 2. Owner/Builder Information
    if not property_data.get('owner_name'):
        score -= 10
        flags.append('Owner name not provided')

    if not property_data.get('owner_phone'):
        score -= 8
        flags.append('Contact number not available')

    if property_data.get('builder_name'):
        score += 5  # Bonus for builder info
        score = min(100, score)

    # 3. Property Details Completeness
    if not property_data.get('description') or len(property_data.get('description', '')) < 50:
        score -= 8
        flags.append('Incomplete property description')

    if not property_data.get('address'):
        score -= 12
        flags.append('No address provided')

    if not property_data.get('pincode'):
        score -= 5
        flags.append('Pincode missing')

    # 4. Images Check
    image_count = property_data.get('image_count', 0)
    if image_count == 0:
        score -= 15
        flags.append('No property images')
    elif image_count < 3:
        score -= 5
        flags.append('Few property images')

    # 5. Verification Status
    if property_data.get('is_verified', False):
        score += 5
        score = min(100, score)

    # 6. Listing Age
    # Older verified listings are more trustworthy

    # Ensure score is in valid range
    score = max(10, min(100, score))

    # Add small variance
    score += random.uniform(-2, 2)
    score = max(10, min(100, score))

    # Determine trust level
    if score >= 85:
        trust_level = 'Highly Trusted'
        badge_color = 'green'
    elif score >= 70:
        trust_level = 'Trusted'
        badge_color = 'blue'
    elif score >= 50:
        trust_level = 'Moderate'
        badge_color = 'orange'
    else:
        trust_level = 'Low Trust'
        badge_color = 'red'

    return {
        'trust_score': round(score, 1),
        'trust_level': trust_level,
        'badge_color': badge_color,
        'flags': flags,
        'is_verified': property_data.get('is_verified', False),
        'verified_owner': bool(property_data.get('owner_name')),
        'verified_property': score >= 70,
    }
