"""
INFY Nest Real Estate - Admin Panel Routes
Property management, user management, analytics
"""
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from functools import wraps
from extensions import db
from models import (User, Property, City, State, PropertyImage,
                    ChatSession, PredictionHistory, SavedProperty)
from ai_modules.price_predictor import format_indian_price

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with analytics"""
    total_users = User.query.count()
    total_properties = Property.query.count()
    total_cities = City.query.count()
    total_states = State.query.count()
    total_chats = ChatSession.query.count()
    total_predictions = PredictionHistory.query.count()
    total_saved = SavedProperty.query.count()

    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()

    # Stats by role
    buyers = User.query.filter_by(role='buyer').count()
    agents = User.query.filter_by(role='agent').count()
    admins = User.query.filter_by(role='admin').count()

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_properties=total_properties,
                           total_cities=total_cities,
                           total_states=total_states,
                           total_chats=total_chats,
                           total_predictions=total_predictions,
                           total_saved=total_saved,
                           recent_users=recent_users,
                           recent_properties=recent_properties,
                           buyers=buyers, agents=agents, admins=admins,
                           format_price=format_indian_price)


@admin_bp.route('/properties')
@login_required
@admin_required
def properties():
    """Manage properties"""
    page = request.args.get('page', 1, type=int)
    properties_list = Property.query.order_by(Property.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/properties.html',
                           properties=properties_list,
                           format_price=format_indian_price)


@admin_bp.route('/properties/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_property():
    """Add new property"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        property_type = request.form.get('property_type', '')
        price = float(request.form.get('price', 0))
        area_sqft = float(request.form.get('area_sqft', 0))
        bedrooms = int(request.form.get('bedrooms', 0))
        bathrooms = int(request.form.get('bathrooms', 0))
        floor_number = int(request.form.get('floor_number', 0))
        total_floors = int(request.form.get('total_floors', 1))
        property_age = int(request.form.get('property_age', 0))
        facing = request.form.get('facing', '')
        furnished = request.form.get('furnished', 'unfurnished')
        city_id = int(request.form.get('city_id', 0))
        locality = request.form.get('locality', '').strip()
        address = request.form.get('address', '').strip()
        pincode = request.form.get('pincode', '').strip()

        # Amenities
        car_parking = 'car_parking' in request.form
        swimming_pool = 'swimming_pool' in request.form
        power_backup = 'power_backup' in request.form
        lift = 'lift' in request.form
        gym = 'gym' in request.form
        club_house = 'club_house' in request.form
        garden = 'garden' in request.form
        security = 'security' in request.form
        children_play_area = 'children_play_area' in request.form
        water_facility = 'water_facility' in request.form
        pet_friendly = 'pet_friendly' in request.form
        near_school = 'near_school' in request.form
        near_hospital = 'near_hospital' in request.form
        metro_connectivity = 'metro_connectivity' in request.form

        # Builder/Owner
        builder_name = request.form.get('builder_name', '').strip()
        owner_name = request.form.get('owner_name', '').strip()
        owner_phone = request.form.get('owner_phone', '').strip()

        # Status
        is_featured = 'is_featured' in request.form
        listing_type = request.form.get('listing_type', 'sale')

        # Validation
        if not title or not price or not area_sqft or not city_id:
            flash('Please fill in all required fields.', 'danger')
            states = State.query.order_by(State.name).all()
            return render_template('admin/add_property.html', states=states)

        # Create property
        prop = Property(
            title=title, description=description, property_type=property_type,
            price=price, area_sqft=area_sqft, bedrooms=bedrooms,
            bathrooms=bathrooms, floor_number=floor_number,
            total_floors=total_floors, property_age=property_age,
            facing=facing, furnished=furnished, city_id=city_id,
            locality=locality, address=address, pincode=pincode,
            car_parking=car_parking, swimming_pool=swimming_pool,
            power_backup=power_backup, lift=lift, gym=gym,
            club_house=club_house, garden=garden, security=security,
            children_play_area=children_play_area, water_facility=water_facility,
            pet_friendly=pet_friendly, near_school=near_school,
            near_hospital=near_hospital, metro_connectivity=metro_connectivity,
            builder_name=builder_name, owner_name=owner_name,
            owner_phone=owner_phone, is_featured=is_featured,
            listing_type=listing_type, is_verified=True
        )

        db.session.add(prop)
        db.session.commit()

        # Handle image uploads
        files = request.files.getlist('images')
        for i, file in enumerate(files):
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"prop_{prop.id}_{i}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                img = PropertyImage(
                    property_id=prop.id,
                    filename=filename,
                    image_type='main' if i == 0 else 'general',
                    is_primary=(i == 0)
                )
                db.session.add(img)

        db.session.commit()
        flash(f'Property "{title}" added successfully!', 'success')
        return redirect(url_for('admin.properties'))

    states = State.query.order_by(State.name).all()
    property_types = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Warehouse', 'Land', 'Plots', 'Luxury Villa',
                      'Gated Community House']
    return render_template('admin/add_property.html',
                           states=states, property_types=property_types)


@admin_bp.route('/properties/edit/<int:property_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_property(property_id):
    """Edit existing property"""
    prop = Property.query.get_or_404(property_id)

    if request.method == 'POST':
        prop.title = request.form.get('title', prop.title).strip()
        prop.description = request.form.get('description', prop.description).strip()
        prop.property_type = request.form.get('property_type', prop.property_type)
        prop.price = float(request.form.get('price', prop.price))
        prop.area_sqft = float(request.form.get('area_sqft', prop.area_sqft))
        prop.bedrooms = int(request.form.get('bedrooms', prop.bedrooms))
        prop.bathrooms = int(request.form.get('bathrooms', prop.bathrooms))
        prop.property_age = int(request.form.get('property_age', prop.property_age))
        prop.furnished = request.form.get('furnished', prop.furnished)
        prop.locality = request.form.get('locality', prop.locality).strip()
        prop.is_featured = 'is_featured' in request.form

        # Amenities
        prop.car_parking = 'car_parking' in request.form
        prop.swimming_pool = 'swimming_pool' in request.form
        prop.power_backup = 'power_backup' in request.form
        prop.lift = 'lift' in request.form
        prop.gym = 'gym' in request.form
        prop.club_house = 'club_house' in request.form
        prop.garden = 'garden' in request.form
        prop.security = 'security' in request.form
        prop.children_play_area = 'children_play_area' in request.form
        prop.water_facility = 'water_facility' in request.form
        prop.pet_friendly = 'pet_friendly' in request.form
        prop.near_school = 'near_school' in request.form
        prop.near_hospital = 'near_hospital' in request.form
        prop.metro_connectivity = 'metro_connectivity' in request.form

        # Handle new image uploads
        files = request.files.getlist('images')
        for i, file in enumerate(files):
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"prop_{prop.id}_{i}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                img = PropertyImage(
                    property_id=prop.id,
                    filename=filename,
                    image_type='general'
                )
                db.session.add(img)

        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('admin.properties'))

    states = State.query.order_by(State.name).all()
    images = PropertyImage.query.filter_by(property_id=property_id).all()
    property_types = ['Apartment', 'Villa', 'Independent House', 'Farm House',
                      'Studio Apartment', 'Penthouse', 'Commercial Office',
                      'Shop', 'Warehouse', 'Land', 'Plots', 'Luxury Villa',
                      'Gated Community House']
    return render_template('admin/edit_property.html',
                           property=prop, states=states,
                           images=images, property_types=property_types)


@admin_bp.route('/properties/delete/<int:property_id>', methods=['POST'])
@login_required
@admin_required
def delete_property(property_id):
    """Delete a property"""
    prop = Property.query.get_or_404(property_id)

    # Delete associated images from filesystem
    images = PropertyImage.query.filter_by(property_id=property_id).all()
    for img in images:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], img.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    # Delete from database
    PropertyImage.query.filter_by(property_id=property_id).delete()
    SavedProperty.query.filter_by(property_id=property_id).delete()
    db.session.delete(prop)
    db.session.commit()

    flash('Property deleted successfully.', 'success')
    return redirect(url_for('admin.properties'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users_list = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users_list)


@admin_bp.route('/users/toggle/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    """Activate/deactivate user"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot deactivate your own account.', 'danger')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def change_role(user_id):
    """Change user role"""
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role', 'buyer')
    if new_role in ['admin', 'agent', 'buyer']:
        user.role = new_role
        db.session.commit()
        flash(f'User {user.username} role changed to {new_role}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/images')
@login_required
@admin_required
def images():
    """Manage property images"""
    page = request.args.get('page', 1, type=int)
    images_list = PropertyImage.query.order_by(PropertyImage.created_at.desc())\
        .paginate(page=page, per_page=30, error_out=False)
    return render_template('admin/images.html', images=images_list)


@admin_bp.route('/images/delete/<int:image_id>', methods=['POST'])
@login_required
@admin_required
def delete_image(image_id):
    """Delete a property image"""
    img = PropertyImage.query.get_or_404(image_id)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], img.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(img)
    db.session.commit()
    flash('Image deleted.', 'success')
    return redirect(url_for('admin.images'))


@admin_bp.route('/cities')
@login_required
@admin_required
def cities():
    """Manage cities"""
    states = State.query.order_by(State.name).all()
    return render_template('admin/cities.html', states=states)


@admin_bp.route('/cities/add', methods=['POST'])
@login_required
@admin_required
def add_city():
    """Add a new city"""
    name = request.form.get('name', '').strip()
    state_id = request.form.get('state_id', type=int)
    if name and state_id:
        city = City(name=name, state_id=state_id)
        db.session.add(city)
        db.session.commit()
        flash(f'City "{name}" added.', 'success')
    else:
        flash('City name and state are required.', 'danger')
    return redirect(url_for('admin.cities'))
