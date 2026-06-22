"""
INFY Real Estate - Main Routes
Landing page and public pages
"""
from flask import Blueprint, render_template, request, jsonify
from models import Property, City, State, PropertyImage
from sqlalchemy import func

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page with featured properties and top cities"""
    featured_properties = Property.query.filter_by(is_featured=True).limit(8).all()
    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(12).all()
    top_cities = City.query.join(Property).group_by(City.id).order_by(
        func.count(Property.id).desc()).limit(8).all()
    states = State.query.all()

    total_properties = Property.query.count()
    total_cities = City.query.count()

    return render_template('index.html',
                           featured_properties=featured_properties,
                           recent_properties=recent_properties,
                           top_cities=top_cities,
                           states=states,
                           total_properties=total_properties,
                           total_cities=total_cities)


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


@main_bp.route('/api/cities/<int:state_id>')
def get_cities(state_id):
    """API endpoint to get cities by state"""
    cities = City.query.filter_by(state_id=state_id).order_by(City.name).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in cities])


@main_bp.route('/api/search-suggestions')
def search_suggestions():
    """API endpoint for search autocomplete"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])

    cities = City.query.filter(City.name.ilike(f'%{query}%')).limit(5).all()
    suggestions = [{'type': 'city', 'name': c.name, 'id': c.id} for c in cities]

    return jsonify(suggestions)
