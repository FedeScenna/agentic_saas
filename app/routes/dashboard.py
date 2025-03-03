from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Agent, Report, Subscription

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Render the dashboard home page."""
    # Get counts for dashboard stats
    agent_count = Agent.query.filter_by(user_id=current_user.id).count()
    active_agent_count = Agent.query.filter_by(user_id=current_user.id, status='active').count()
    report_count = Report.query.filter_by(user_id=current_user.id).count()
    completed_report_count = Report.query.filter_by(user_id=current_user.id, status='completed').count()
    
    # Get subscription info
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    
    # Get recent reports
    recent_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).limit(5).all()
    
    # Get agent status
    agents = Agent.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard/index.html',
                          agent_count=agent_count,
                          active_agent_count=active_agent_count,
                          report_count=report_count,
                          completed_report_count=completed_report_count,
                          subscription=subscription,
                          recent_reports=recent_reports,
                          agents=agents)

@dashboard_bp.route('/activity')
@login_required
def activity():
    """Render the activity page showing recent activity."""
    # Get recent reports
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).limit(20).all()
    
    # Get recent agent activity
    agents = Agent.query.filter_by(user_id=current_user.id).order_by(Agent.last_active.desc()).all()
    
    return render_template('dashboard/activity.html',
                          reports=reports,
                          agents=agents)

@dashboard_bp.route('/settings')
@login_required
def settings():
    """Render the settings page."""
    return render_template('dashboard/settings.html') 