from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Subscription

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/')
@login_required
def index():
    """Render the subscription details page."""
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    plans = current_app.config['SUBSCRIPTION_PLANS']
    
    return render_template('subscription/index.html', 
                          subscription=subscription,
                          plans=plans)

@subscription_bp.route('/plans')
@login_required
def plans():
    """Render the subscription plans page."""
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    plans = current_app.config['SUBSCRIPTION_PLANS']
    
    return render_template('subscription/plans.html', 
                          subscription=subscription,
                          plans=plans)

@subscription_bp.route('/subscribe/<plan_type>', methods=['GET', 'POST'])
@login_required
def subscribe(plan_type):
    """Handle subscription to a plan."""
    plans = current_app.config['SUBSCRIPTION_PLANS']
    
    if plan_type not in plans:
        flash('Invalid subscription plan', 'danger')
        return redirect(url_for('subscription.plans'))
    
    # Check if user already has a subscription
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        if subscription:
            # Update existing subscription
            subscription.plan_type = plan_type
            subscription.is_active = True
            subscription.payment_method = payment_method
            subscription.payment_status = 'paid'
            subscription.last_payment_date = datetime.utcnow()
            subscription.next_payment_date = datetime.utcnow() + timedelta(days=30)
            
            if not subscription.start_date:
                subscription.start_date = datetime.utcnow()
            
            subscription.end_date = datetime.utcnow() + timedelta(days=30)
        else:
            # Create new subscription
            subscription = Subscription(
                user_id=current_user.id,
                plan_type=plan_type,
                is_active=True,
                payment_method=payment_method,
                payment_status='paid',
                last_payment_date=datetime.utcnow(),
                next_payment_date=datetime.utcnow() + timedelta(days=30),
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(subscription)
        
        db.session.commit()
        flash(f'Successfully subscribed to {plans[plan_type]["name"]} plan', 'success')
        return redirect(url_for('subscription.index'))
    
    return render_template('subscription/subscribe.html', 
                          plan=plans[plan_type],
                          plan_type=plan_type)

@subscription_bp.route('/cancel', methods=['GET', 'POST'])
@login_required
def cancel():
    """Handle subscription cancellation."""
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    
    if not subscription:
        flash('No active subscription found', 'warning')
        return redirect(url_for('subscription.plans'))
    
    if request.method == 'POST':
        subscription.cancel()
        flash('Your subscription has been cancelled', 'info')
        return redirect(url_for('subscription.index'))
    
    return render_template('subscription/cancel.html', subscription=subscription)

@subscription_bp.route('/upgrade')
@login_required
def upgrade():
    """Render the upgrade subscription page."""
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    plans = current_app.config['SUBSCRIPTION_PLANS']
    
    if not subscription:
        return redirect(url_for('subscription.plans'))
    
    # Filter plans that are higher tier than current
    upgrade_plans = {}
    current_plan_price = plans[subscription.plan_type]['price']
    
    for plan_type, plan in plans.items():
        if plan['price'] > current_plan_price:
            upgrade_plans[plan_type] = plan
    
    return render_template('subscription/upgrade.html', 
                          subscription=subscription,
                          plans=upgrade_plans) 