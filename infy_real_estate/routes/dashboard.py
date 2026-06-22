"""
INFY Nest Real Estate - User Dashboard Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import (Property, SavedProperty, ChatSession, ChatMessage,
                    PredictionHistory, City)
from ai_modules.price_predictor import format_indian_price

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """User dashboard home"""
    saved_count = SavedProperty.query.filter_by(user_id=current_user.id).count()
    chat_count = ChatSession.query.filter_by(user_id=current_user.id).count()
    prediction_count = PredictionHistory.query.filter_by(user_id=current_user.id).count()

    recent_saved = SavedProperty.query.filter_by(user_id=current_user.id)\
        .order_by(SavedProperty.created_at.desc()).limit(5).all()

    recent_predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
        .order_by(PredictionHistory.created_at.desc()).limit(5).all()

    return render_template('dashboard/index.html',
                           saved_count=saved_count,
                           chat_count=chat_count,
                           prediction_count=prediction_count,
                           recent_saved=recent_saved,
                           recent_predictions=recent_predictions,
                           format_price=format_indian_price)


@dashboard_bp.route('/saved')
@login_required
def saved_properties():
    """View saved/favorite properties"""
    saved = SavedProperty.query.filter_by(user_id=current_user.id)\
        .order_by(SavedProperty.created_at.desc()).all()
    return render_template('dashboard/saved.html',
                           saved=saved,
                           format_price=format_indian_price)


@dashboard_bp.route('/predictions')
@login_required
def predictions():
    """View prediction history"""
    history = PredictionHistory.query.filter_by(user_id=current_user.id)\
        .order_by(PredictionHistory.created_at.desc()).all()
    return render_template('dashboard/predictions.html',
                           predictions=history,
                           format_price=format_indian_price)


@dashboard_bp.route('/saved/remove/<int:saved_id>', methods=['POST'])
@login_required
def remove_saved(saved_id):
    """Remove a saved property"""
    saved = SavedProperty.query.get_or_404(saved_id)
    if saved.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard.saved_properties'))

    db.session.delete(saved)
    db.session.commit()
    flash('Property removed from saved list.', 'info')
    return redirect(url_for('dashboard.saved_properties'))
