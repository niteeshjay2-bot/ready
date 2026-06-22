"""
INFY Real Estate - Database Models
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(20), default='buyer')  # admin, agent, buyer
    avatar = db.Column(db.String(256), default='default_avatar.png')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    saved_properties = db.relationship('SavedProperty', backref='user', lazy=True)
    chats = db.relationship('ChatSession', backref='user', lazy=True)
    predictions = db.relationship('PredictionHistory', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10))
    cities = db.relationship('City', backref='state', lazy=True)


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    properties = db.relationship('Property', backref='city', lazy=True)


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    property_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area_sqft = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)
    floor_number = db.Column(db.Integer, default=0)
    total_floors = db.Column(db.Integer, default=1)
    property_age = db.Column(db.Integer, default=0)
    facing = db.Column(db.String(20))
    furnished = db.Column(db.String(20), default='unfurnished')

    # Location
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    locality = db.Column(db.String(200))
    address = db.Column(db.Text)
    pincode = db.Column(db.String(10))

    # Amenities (Boolean)
    car_parking = db.Column(db.Boolean, default=False)
    swimming_pool = db.Column(db.Boolean, default=False)
    power_backup = db.Column(db.Boolean, default=False)
    lift = db.Column(db.Boolean, default=False)
    gym = db.Column(db.Boolean, default=False)
    club_house = db.Column(db.Boolean, default=False)
    garden = db.Column(db.Boolean, default=False)
    security = db.Column(db.Boolean, default=False)
    children_play_area = db.Column(db.Boolean, default=False)
    water_facility = db.Column(db.Boolean, default=False)
    pet_friendly = db.Column(db.Boolean, default=False)
    near_school = db.Column(db.Boolean, default=False)
    near_hospital = db.Column(db.Boolean, default=False)
    metro_connectivity = db.Column(db.Boolean, default=False)

    # Builder / Owner
    builder_name = db.Column(db.String(150))
    owner_name = db.Column(db.String(150))
    owner_phone = db.Column(db.String(15))

    # AI Scores
    investment_score = db.Column(db.Float, default=0)
    trust_score = db.Column(db.Float, default=0)
    growth_potential = db.Column(db.String(20), default='Medium')

    # Status
    is_verified = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    listing_type = db.Column(db.String(10), default='sale')  # sale, rent
    status = db.Column(db.String(20), default='available')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    images = db.relationship('PropertyImage', backref='property', lazy=True)


class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(512))  # External image URL (e.g. Unsplash)
    image_type = db.Column(db.String(50), default='general')  # main, living_room, bedroom, kitchen, general
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SavedProperty(db.Model):
    __tablename__ = 'saved_properties'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    property = db.relationship('Property', backref='saved_by')


class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), default='New Chat')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('ChatMessage', backref='session', lazy=True, order_by='ChatMessage.created_at')


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # user, assistant
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String(100))
    area_sqft = db.Column(db.Float)
    property_type = db.Column(db.String(50))
    bedrooms = db.Column(db.Integer)
    current_price = db.Column(db.Float)
    price_1year = db.Column(db.Float)
    price_3year = db.Column(db.Float)
    price_5year = db.Column(db.Float)
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
