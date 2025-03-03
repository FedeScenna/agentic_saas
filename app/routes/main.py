from flask import Blueprint, render_template, current_app
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the home page."""
    return render_template('main/index.html')

@main_bp.route('/features')
def features():
    """Render the features page."""
    return render_template('main/features.html')

@main_bp.route('/pricing')
def pricing():
    """Render the pricing page."""
    plans = current_app.config.get('SUBSCRIPTION_PLANS', {})
    return render_template('main/pricing.html', plans=plans)

@main_bp.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('main/contact.html')

@main_bp.route('/faq')
def faq():
    """Render the FAQ page."""
    return render_template('main/faq.html')

@main_bp.route('/terms')
def terms():
    """Render the terms of service page."""
    return render_template('main/terms.html')

@main_bp.route('/privacy')
def privacy():
    """Render the privacy policy page."""
    return render_template('main/privacy.html') 