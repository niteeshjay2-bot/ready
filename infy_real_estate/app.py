"""
INFY Real Estate - India's Smartest AI Powered Real Estate Platform
Main Application Entry Point
"""
import os
from flask import Flask
from config import Config
from extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.properties import properties_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp
    from routes.ai_routes import ai_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(properties_bp, url_prefix='/properties')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ai_bp, url_prefix='/ai')

    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Import models to ensure they are registered
    from models import User, State, City, Property, PropertyImage, SavedProperty, ChatSession, ChatMessage, PredictionHistory

    # Register template globals
    from ai_modules.price_predictor import format_indian_price
    app.jinja_env.globals['format_price'] = format_indian_price

    with app.app_context():
        db.create_all()
        # Auto-seed if database is empty
        from models import Property, State
        if State.query.count() == 0:
            _auto_seed(app)

    return app


def _auto_seed(app):
    """Auto-populate database with seed data on first run"""
    import random
    from models import User, State, City, Property, PropertyImage

    print("Database is empty. Auto-seeding with sample data...")

    STATES_CITIES = {
        'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Tirupati', 'Kakinada', 'Guntur'],
        'Telangana': ['Hyderabad', 'Warangal', 'Karimnagar', 'Nizamabad', 'Khammam'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem'],
        'Karnataka': ['Bengaluru', 'Mysuru', 'Mangaluru', 'Hubli', 'Belgaum'],
        'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'Kollam'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar'],
        'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer'],
        'Uttar Pradesh': ['Lucknow', 'Noida', 'Agra', 'Varanasi', 'Kanpur'],
        'Madhya Pradesh': ['Indore', 'Bhopal', 'Jabalpur', 'Gwalior', 'Ujjain'],
        'West Bengal': ['Kolkata', 'Siliguri', 'Durgapur', 'Asansol', 'Howrah'],
        'Bihar': ['Patna', 'Gaya', 'Muzaffarpur', 'Bhagalpur', 'Darbhanga'],
        'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur'],
        'Punjab': ['Chandigarh', 'Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala'],
        'Haryana': ['Gurgaon', 'Faridabad', 'Panipat', 'Karnal', 'Hisar'],
        'Delhi': ['New Delhi', 'Dwarka', 'Rohini', 'Saket', 'Janakpuri'],
        'Jharkhand': ['Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro', 'Hazaribagh'],
        'Chhattisgarh': ['Raipur', 'Bhilai', 'Bilaspur', 'Korba', 'Durg'],
        'Assam': ['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon'],
        'Uttarakhand': ['Dehradun', 'Haridwar', 'Rishikesh', 'Haldwani', 'Roorkee'],
        'Himachal Pradesh': ['Shimla', 'Manali', 'Dharamshala', 'Solan', 'Mandi'],
        'Goa': ['Panaji', 'Margao', 'Vasco da Gama', 'Mapusa', 'Ponda'],
        'Jammu and Kashmir': ['Srinagar', 'Jammu', 'Anantnag', 'Baramulla', 'Udhampur'],
        'Tripura': ['Agartala', 'Dharmanagar'],
        'Meghalaya': ['Shillong', 'Tura'],
        'Manipur': ['Imphal', 'Thoubal'],
        'Mizoram': ['Aizawl', 'Lunglei'],
        'Nagaland': ['Kohima', 'Dimapur'],
        'Arunachal Pradesh': ['Itanagar', 'Naharlagun'],
        'Sikkim': ['Gangtok', 'Namchi'],
        'Ladakh': ['Leh', 'Kargil'],
        'Puducherry': ['Puducherry', 'Karaikal'],
    }

    PROPERTY_TYPES = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Land', 'Plots', 'Luxury Villa', 'Gated Community House']

    LOCALITIES = {
        'Hyderabad': ['Gachibowli', 'HITEC City', 'Banjara Hills', 'Jubilee Hills', 'Kondapur', 'Madhapur'],
        'Bengaluru': ['Whitefield', 'Electronic City', 'Koramangala', 'HSR Layout', 'Indiranagar', 'Sarjapur Road'],
        'Mumbai': ['Andheri', 'Bandra', 'Powai', 'Worli', 'Malad', 'Goregaon'],
        'Chennai': ['OMR', 'Anna Nagar', 'T Nagar', 'Adyar', 'Velachery', 'Sholinganallur'],
        'Pune': ['Hinjewadi', 'Wakad', 'Kharadi', 'Baner', 'Viman Nagar', 'Hadapsar'],
        'Delhi': ['Dwarka', 'Rohini', 'Saket', 'Vasant Kunj', 'Janakpuri'],
        'Kolkata': ['Salt Lake', 'New Town', 'Rajarhat', 'Howrah'],
        'Ahmedabad': ['SG Highway', 'Bodakdev', 'Satellite', 'Prahlad Nagar'],
        'Jaipur': ['Vaishali Nagar', 'Mansarovar', 'C-Scheme', 'Malviya Nagar'],
        'Gurgaon': ['Golf Course Road', 'Sohna Road', 'MG Road', 'Sector 49'],
        'Noida': ['Sector 150', 'Sector 137', 'Sector 75', 'Greater Noida'],
    }

    BUILDERS = ['DLF Group', 'Prestige Constructions', 'Godrej Properties', 'Sobha Developers',
                'Brigade Group', 'Lodha Group', 'Oberoi Realty', 'Mahindra Lifespaces',
                'Tata Housing', 'Puravankara', 'Shapoorji Pallonji', 'Aparna Constructions']

    OWNER_NAMES = ['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Sunita Reddy', 'Vikram Singh',
                   'Deepa Nair', 'Suresh Iyer', 'Kavitha Rao', 'Anil Kapoor', 'Meera Joshi']

    # Create admin user
    admin = User(username='admin', email='admin@infy.com', full_name='INFY Admin',
                 phone='9876543210', role='admin', is_active=True)
    admin.set_password('admin123')
    db.session.add(admin)

    buyer = User(username='buyer1', email='buyer@infy.com', full_name='Rahul Sharma',
                 phone='9876543211', role='buyer', is_active=True)
    buyer.set_password('buyer123')
    db.session.add(buyer)

    agent = User(username='agent1', email='agent@infy.com', full_name='Priya Agent',
                 phone='9876543212', role='agent', is_active=True)
    agent.set_password('agent123')
    db.session.add(agent)
    db.session.commit()

    # Create states and cities
    city_objects = {}
    for state_name, cities in STATES_CITIES.items():
        state = State(name=state_name)
        db.session.add(state)
        db.session.flush()
        for city_name in cities:
            city = City(name=city_name, state_id=state.id)
            db.session.add(city)
            db.session.flush()
            city_objects[city_name] = city.id
    db.session.commit()

    # Create properties
    major_cities = ['Hyderabad', 'Bengaluru', 'Mumbai', 'Chennai', 'Pune',
                    'Delhi', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Gurgaon', 'Noida']
    property_count = 0

    for city_name, city_id in city_objects.items():
        num_properties = random.randint(8, 12) if city_name in major_cities else random.randint(2, 4)

        for i in range(num_properties):
            ptype = random.choice(PROPERTY_TYPES)
            bedrooms = random.randint(1, 5) if ptype not in ['Land', 'Plots', 'Shop'] else 0
            bathrooms = max(1, bedrooms - random.randint(0, 1)) if bedrooms > 0 else 0

            base_prices = {'Mumbai': 15000, 'Delhi': 12000, 'Bengaluru': 8000,
                           'Hyderabad': 6500, 'Chennai': 7000, 'Pune': 7500,
                           'Gurgaon': 10000, 'Noida': 7000, 'Kolkata': 5500}
            base = base_prices.get(city_name, random.randint(3000, 6000))
            area = random.choice([800, 1000, 1200, 1500, 1800, 2000, 2500, 3000])

            type_mult = {'Villa': 1.8, 'Luxury Villa': 2.5, 'Penthouse': 2.2,
                         'Farm House': 1.5, 'Apartment': 1.0, 'Studio Apartment': 0.85,
                         'Independent House': 1.3, 'Gated Community House': 1.5,
                         'Commercial Office': 1.4, 'Shop': 1.2, 'Land': 0.4, 'Plots': 0.45}
            mult = type_mult.get(ptype, 1.0)
            price = base * area * mult * random.uniform(0.85, 1.15)

            locality = random.choice(LOCALITIES.get(city_name, [f'{city_name} Central', f'{city_name} East', f'{city_name} West']))

            title_templates = [
                f"Premium {bedrooms} BHK {ptype} in {locality}",
                f"Luxurious {ptype} at {locality}, {city_name}",
                f"{bedrooms} BHK {ptype} with Modern Amenities",
                f"Spacious {ptype} in Prime Location {locality}",
                f"Beautiful {bedrooms} BHK {ptype} - Ready to Move",
            ]

            prop = Property(
                title=random.choice(title_templates),
                description=f"A beautiful {bedrooms} BHK {ptype} in {locality}, {city_name}. Features modern amenities and excellent connectivity.",
                property_type=ptype, price=round(price, 0), area_sqft=area,
                bedrooms=bedrooms, bathrooms=bathrooms,
                floor_number=random.randint(1, 15), total_floors=random.randint(5, 25),
                property_age=random.randint(0, 15),
                facing=random.choice(['North', 'South', 'East', 'West', 'North-East']),
                furnished=random.choice(['unfurnished', 'semi-furnished', 'furnished']),
                city_id=city_id, locality=locality,
                address=f"{random.randint(1,500)}, {locality}, {city_name}",
                pincode=str(random.randint(100000, 999999)),
                car_parking=random.choice([True, True, False]),
                swimming_pool=random.choice([True, False, False]),
                power_backup=random.choice([True, True, False]),
                lift=random.choice([True, True, False]),
                gym=random.choice([True, False]),
                club_house=random.choice([True, False, False]),
                garden=random.choice([True, False]),
                security=random.choice([True, True, True, False]),
                children_play_area=random.choice([True, False]),
                water_facility=random.choice([True, True, False]),
                pet_friendly=random.choice([True, False, False]),
                near_school=random.choice([True, True, False]),
                near_hospital=random.choice([True, False]),
                metro_connectivity=random.choice([True, False]),
                builder_name=random.choice(BUILDERS),
                owner_name=random.choice(OWNER_NAMES),
                owner_phone=f"9{random.randint(100000000, 999999999)}",
                investment_score=round(random.uniform(55, 95), 1),
                trust_score=round(random.uniform(70, 98), 1),
                growth_potential=random.choice(['Low', 'Medium', 'High', 'Very High']),
                is_verified=random.choice([True, True, True, False]),
                is_featured=(i < 2),
                listing_type=random.choice(['sale', 'sale', 'sale', 'rent']),
            )
            db.session.add(prop)
            property_count += 1

    db.session.commit()

    # Create property images
    properties = Property.query.all()
    for prop in properties:
        num_imgs = random.randint(1, 4)
        img_types = ['main', 'living_room', 'bedroom', 'kitchen']
        for j in range(num_imgs):
            img = PropertyImage(
                property_id=prop.id,
                filename=f"property_{prop.id}_{j+1}.svg",
                image_type=img_types[j] if j < len(img_types) else 'general',
                is_primary=(j == 0)
            )
            db.session.add(img)
    db.session.commit()

    print(f"Auto-seed complete! Created {len(STATES_CITIES)} states, {len(city_objects)} cities, {property_count} properties")
    print(f"Login: admin@infy.com / admin123")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
