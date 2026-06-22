"""
INFY Nest Real Estate - Seed Data
Populates database with states, cities, properties, and admin user
"""
import random
from app import create_app
from extensions import db
from models import User, State, City, Property, PropertyImage

app = create_app()

# All Indian States and Union Territories with cities
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
    'Tripura': ['Agartala', 'Dharmanagar', 'Udaipur', 'Kailashahar', 'Belonia'],
    'Meghalaya': ['Shillong', 'Tura', 'Jowai', 'Nongstoin', 'Williamnagar'],
    'Manipur': ['Imphal', 'Thoubal', 'Bishnupur', 'Churachandpur', 'Kakching'],
    'Mizoram': ['Aizawl', 'Lunglei', 'Champhai', 'Serchhip', 'Kolasib'],
    'Nagaland': ['Kohima', 'Dimapur', 'Mokokchung', 'Tuensang', 'Wokha'],
    'Arunachal Pradesh': ['Itanagar', 'Naharlagun', 'Pasighat', 'Tawang', 'Ziro'],
    'Sikkim': ['Gangtok', 'Namchi', 'Gyalshing', 'Mangan', 'Rangpo'],
    'Ladakh': ['Leh', 'Kargil'],
    'Puducherry': ['Puducherry', 'Karaikal'],
    'Chandigarh': ['Chandigarh'],
    'Andaman and Nicobar': ['Port Blair'],
    'Dadra and Nagar Haveli': ['Silvassa'],
    'Lakshadweep': ['Kavaratti'],
}


PROPERTY_TYPES = [
    'Apartment', 'Villa', 'Independent House', 'Farm House',
    'Studio Apartment', 'Penthouse', 'Commercial Office',
    'Shop', 'Warehouse', 'Land', 'Plots', 'Luxury Villa',
    'Gated Community House'
]

LOCALITIES = {
    'Hyderabad': ['Gachibowli', 'HITEC City', 'Banjara Hills', 'Jubilee Hills', 'Kondapur', 'Madhapur', 'Kukatpally'],
    'Bengaluru': ['Whitefield', 'Electronic City', 'Koramangala', 'HSR Layout', 'Indiranagar', 'Marathahalli', 'Sarjapur Road'],
    'Mumbai': ['Andheri', 'Bandra', 'Powai', 'Worli', 'Malad', 'Goregaon', 'Thane'],
    'Chennai': ['OMR', 'Anna Nagar', 'T Nagar', 'Adyar', 'Velachery', 'Porur', 'Sholinganallur'],
    'Pune': ['Hinjewadi', 'Wakad', 'Kharadi', 'Baner', 'Viman Nagar', 'Hadapsar', 'Kothrud'],
    'Delhi': ['Dwarka', 'Rohini', 'Saket', 'Vasant Kunj', 'Janakpuri', 'Pitampura'],
    'Kolkata': ['Salt Lake', 'New Town', 'Rajarhat', 'Howrah', 'Dum Dum'],
    'Ahmedabad': ['SG Highway', 'Bodakdev', 'Satellite', 'Prahlad Nagar', 'Vastrapur'],
    'Jaipur': ['Vaishali Nagar', 'Mansarovar', 'C-Scheme', 'Malviya Nagar', 'Tonk Road'],
    'Gurgaon': ['Golf Course Road', 'Sohna Road', 'MG Road', 'Sector 49', 'Sector 56'],
    'Noida': ['Sector 150', 'Sector 137', 'Sector 75', 'Sector 44', 'Greater Noida'],
}

BUILDERS = [
    'DLF Group', 'Prestige Constructions', 'Godrej Properties', 'Sobha Developers',
    'Brigade Group', 'Lodha Group', 'Oberoi Realty', 'Mahindra Lifespaces',
    'Tata Housing', 'Puravankara', 'Shapoorji Pallonji', 'Hiranandani',
    'Rustomjee', 'K Raheja Corp', 'Emaar India', 'RERA Approved Builder',
    'Aparna Constructions', 'My Home Group', 'Ramky Group', 'Sai Properties',
]

OWNER_NAMES = [
    'Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Sunita Reddy', 'Vikram Singh',
    'Deepa Nair', 'Suresh Iyer', 'Kavitha Rao', 'Anil Kapoor', 'Meera Joshi',
    'Rahul Gupta', 'Anita Desai', 'Prakash Mehta', 'Lakshmi Venkat', 'Mohan Das',
]


def generate_property_title(ptype, bedrooms, locality, city):
    """Generate a realistic property title"""
    templates = [
        f"Premium {bedrooms} BHK {ptype} in {locality}",
        f"Luxurious {ptype} at {locality}, {city}",
        f"{bedrooms} BHK {ptype} with Modern Amenities",
        f"Spacious {ptype} in Prime Location {locality}",
        f"Beautiful {bedrooms} BHK {ptype} - Ready to Move",
        f"Brand New {ptype} in {locality}",
        f"Elegant {bedrooms} BHK {ptype} Near IT Hub",
        f"Well-Maintained {ptype} in Gated Community",
    ]
    return random.choice(templates)


def generate_description(ptype, bedrooms, locality, city):
    """Generate property description"""
    descs = [
        f"This stunning {bedrooms} BHK {ptype} is located in the heart of {locality}, {city}. "
        f"Features modern architecture, premium fittings, and excellent connectivity. "
        f"Ideal for families looking for a comfortable lifestyle with world-class amenities.",

        f"A premium {ptype} offering {bedrooms} spacious bedrooms with attached bathrooms. "
        f"Located in {locality} with easy access to schools, hospitals, and IT parks. "
        f"The property features high-quality construction and modern design.",

        f"Discover luxury living in this {bedrooms} BHK {ptype} at {locality}. "
        f"Built with premium materials, this property offers a perfect blend of comfort and style. "
        f"Enjoy proximity to major landmarks and excellent public transport connectivity.",
    ]
    return random.choice(descs)


def seed_database():
    """Main seed function"""
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()

        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@infy.com',
            full_name='INFY Admin',
            phone='9876543210',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create sample buyer
        buyer = User(
            username='buyer1',
            email='buyer@infy.com',
            full_name='Rahul Sharma',
            phone='9876543211',
            role='buyer',
            is_active=True
        )
        buyer.set_password('buyer123')
        db.session.add(buyer)

        # Create agent
        agent = User(
            username='agent1',
            email='agent@infy.com',
            full_name='Priya Agent',
            phone='9876543212',
            role='agent',
            is_active=True
        )
        agent.set_password('agent123')
        db.session.add(agent)
        db.session.commit()
        print(f"Created 3 users (admin, buyer, agent)")


        # Create States and Cities
        print("Creating states and cities...")
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
        total_cities = sum(len(c) for c in STATES_CITIES.values())
        print(f"Created {len(STATES_CITIES)} states, {total_cities} cities")

        # Create Properties
        print("Creating properties...")
        property_count = 0
        # Major cities get more properties
        major_cities = ['Hyderabad', 'Bengaluru', 'Mumbai', 'Chennai', 'Pune',
                        'Delhi', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Gurgaon', 'Noida']

        for city_name, city_id in city_objects.items():
            if city_name in major_cities:
                num_properties = random.randint(8, 12)
            else:
                num_properties = random.randint(2, 5)

            for i in range(num_properties):
                ptype = random.choice(PROPERTY_TYPES)
                bedrooms = random.randint(1, 5) if ptype not in ['Land', 'Plots', 'Shop', 'Warehouse'] else 0
                bathrooms = max(1, bedrooms - random.randint(0, 1)) if bedrooms > 0 else 0

                # Price based on city and type
                base_prices = {
                    'Mumbai': 15000, 'Delhi': 12000, 'Bengaluru': 8000,
                    'Hyderabad': 6500, 'Chennai': 7000, 'Pune': 7500,
                    'Gurgaon': 10000, 'Noida': 7000, 'Kolkata': 5500,
                }
                base = base_prices.get(city_name, random.randint(3000, 6000))
                area = random.choice([800, 1000, 1200, 1500, 1800, 2000, 2500, 3000, 3500])

                type_mult = {'Villa': 1.8, 'Luxury Villa': 2.5, 'Penthouse': 2.2,
                             'Farm House': 1.5, 'Apartment': 1.0, 'Studio Apartment': 0.85,
                             'Independent House': 1.3, 'Gated Community House': 1.5,
                             'Commercial Office': 1.4, 'Shop': 1.2, 'Warehouse': 0.5,
                             'Land': 0.4, 'Plots': 0.45}
                mult = type_mult.get(ptype, 1.0)
                price = base * area * mult * random.uniform(0.85, 1.15)

                locality = random.choice(LOCALITIES.get(city_name, [f'{city_name} Central', f'{city_name} East', f'{city_name} West']))

                prop = Property(
                    title=generate_property_title(ptype, bedrooms, locality, city_name),
                    description=generate_description(ptype, bedrooms, locality, city_name),
                    property_type=ptype,
                    price=round(price, 0),
                    area_sqft=area,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    floor_number=random.randint(1, 15),
                    total_floors=random.randint(5, 30),
                    property_age=random.randint(0, 15),
                    facing=random.choice(['North', 'South', 'East', 'West', 'North-East']),
                    furnished=random.choice(['unfurnished', 'semi-furnished', 'furnished']),
                    city_id=city_id,
                    locality=locality,
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
                    is_featured=(i < 2),  # First 2 in each major city are featured
                    listing_type=random.choice(['sale', 'sale', 'sale', 'rent']),
                )
                db.session.add(prop)
                property_count += 1

        db.session.commit()
        print(f"Created {property_count} properties")

        # Real property image URLs from Unsplash (free to use)
        PROPERTY_IMAGE_URLS = {
            'main': [
                'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80',
                'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80',
                'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
                'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=80',
                'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80',
                'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&q=80',
                'https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?w=800&q=80',
                'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800&q=80',
                'https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800&q=80',
                'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=80',
                'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
                'https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=800&q=80',
                'https://images.unsplash.com/photo-1602343168051-4f784a945b44?w=800&q=80',
                'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
                'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&q=80',
                'https://images.unsplash.com/photo-1599809275671-b5942cabc7a2?w=800&q=80',
                'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&q=80',
                'https://images.unsplash.com/photo-1576941089067-2de3c901e126?w=800&q=80',
                'https://images.unsplash.com/photo-1598228723793-52759bba239c?w=800&q=80',
                'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&q=80',
            ],
            'living_room': [
                'https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=800&q=80',
                'https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?w=800&q=80',
                'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80',
                'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80',
                'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80',
                'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800&q=80',
                'https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=800&q=80',
                'https://images.unsplash.com/photo-1616486338812-3dadae5b4ace?w=800&q=80',
                'https://images.unsplash.com/photo-1618219908412-a29a1bb7b86e?w=800&q=80',
                'https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&q=80',
                'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&q=80',
                'https://images.unsplash.com/photo-1567767292784-4022b30ff2b2?w=800&q=80',
                'https://images.unsplash.com/photo-1615529328331-f8917597711f?w=800&q=80',
                'https://images.unsplash.com/photo-1600210491369-e753d80a41f3?w=800&q=80',
                'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&q=80',
            ],
            'bedroom': [
                'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
                'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&q=80',
                'https://images.unsplash.com/photo-1617325247661-675ab386e5bb?w=800&q=80',
                'https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=800&q=80',
                'https://images.unsplash.com/photo-1522771739806-4e41a8ae467a?w=800&q=80',
                'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80',
                'https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=800&q=80',
                'https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=800&q=80',
                'https://images.unsplash.com/photo-1615874959474-d609969a20ed?w=800&q=80',
                'https://images.unsplash.com/photo-1574643156929-51fa098b0394?w=800&q=80',
                'https://images.unsplash.com/photo-1590490360182-c33d7b6b2feb?w=800&q=80',
                'https://images.unsplash.com/photo-1600566753151-384129cf4e3e?w=800&q=80',
                'https://images.unsplash.com/photo-1612320648774-0a1f0626e8b4?w=800&q=80',
                'https://images.unsplash.com/photo-1621891334261-cbbe9be1d7c2?w=800&q=80',
                'https://images.unsplash.com/photo-1617098474202-0d0d7f60c56b?w=800&q=80',
            ],
            'kitchen': [
                'https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=800&q=80',
                'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
                'https://images.unsplash.com/photo-1600566752734-2a0cd66c42f7?w=800&q=80',
                'https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=800&q=80',
                'https://images.unsplash.com/photo-1600585152915-d208bec867a1?w=800&q=80',
                'https://images.unsplash.com/photo-1574739782594-db4ead022697?w=800&q=80',
                'https://images.unsplash.com/photo-1588854337236-6889d631faa8?w=800&q=80',
                'https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=800&q=80',
                'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
                'https://images.unsplash.com/photo-1596205836109-7b5a9d58cff1?w=800&q=80',
                'https://images.unsplash.com/photo-1600489000022-c2086d79f9d4?w=800&q=80',
                'https://images.unsplash.com/photo-1615529328331-f8917597711f?w=800&q=80',
                'https://images.unsplash.com/photo-1560185007-5f0bb1866cab?w=800&q=80',
                'https://images.unsplash.com/photo-1613545325278-f24b0cae1224?w=800&q=80',
                'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=800&q=80',
            ],
        }

        # Create property images with real URLs
        print("Creating property image records with real image URLs...")
        properties = Property.query.all()
        img_count = 0
        for prop in properties:
            # Each property gets 1-4 images
            num_imgs = random.randint(1, 4)
            img_types = ['main', 'living_room', 'bedroom', 'kitchen']
            for j in range(num_imgs):
                img_type = img_types[j] if j < len(img_types) else 'general'
                url_list = PROPERTY_IMAGE_URLS.get(img_type, PROPERTY_IMAGE_URLS['main'])
                image_url = random.choice(url_list)
                img = PropertyImage(
                    property_id=prop.id,
                    filename=f"property_{prop.id}_{j+1}.svg",
                    image_url=image_url,
                    image_type=img_type,
                    is_primary=(j == 0)
                )
                db.session.add(img)
                img_count += 1

        db.session.commit()
        print(f"Created {img_count} image records with real URLs")
        print(f"\nSeed complete! Total: {len(STATES_CITIES)} states, {total_cities} cities, {property_count} properties")
        print(f"\nLogin credentials:")
        print(f"  Admin: admin@infy.com / admin123")
        print(f"  Buyer: buyer@infy.com / buyer123")
        print(f"  Agent: agent@infy.com / agent123")


if __name__ == '__main__':
    seed_database()
