from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Report, Agent, Visualization

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def index():
    """Render the reports list page."""
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()
    return render_template('reports/index.html', reports=reports)

@reports_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Handle report creation."""
    # Get available agents
    agents = Agent.query.filter_by(user_id=current_user.id, status='active').all()
    
    if not agents:
        flash('You need at least one active agent to create reports', 'warning')
        return redirect(url_for('agents.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        agent_id = request.form.get('agent_id')
        report_type = request.form.get('report_type')
        
        # Validate agent belongs to user
        agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first()
        if not agent:
            flash('Invalid agent selected', 'danger')
            return redirect(url_for('reports.create'))
        
        report = Report(
            user_id=current_user.id,
            agent_id=agent_id,
            title=title,
            description=description,
            report_type=report_type,
            status='pending',
            data={}
        )
        
        db.session.add(report)
        db.session.commit()
        
        flash('Report created successfully', 'success')
        return redirect(url_for('reports.view', report_id=report.id))
    
    return render_template('reports/create.html', agents=agents)

@reports_bp.route('/<int:report_id>')
@login_required
def view(report_id):
    """View report details."""
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    agent = Agent.query.filter_by(id=report.agent_id).first()
    visualizations = Visualization.query.filter_by(report_id=report.id).all()
    
    return render_template('reports/view.html', 
                          report=report, 
                          agent=agent,
                          visualizations=visualizations)

@reports_bp.route('/<int:report_id>/delete', methods=['POST'])
@login_required
def delete(report_id):
    """Delete a report."""
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    
    # Delete associated visualizations
    Visualization.query.filter_by(report_id=report.id).delete()
    
    db.session.delete(report)
    db.session.commit()
    
    flash('Report deleted successfully', 'success')
    return redirect(url_for('reports.index'))

@reports_bp.route('/<int:report_id>/visualizations/create', methods=['GET', 'POST'])
@login_required
def create_visualization(report_id):
    """Create a new visualization for a report."""
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    
    if not report.is_completed:
        flash('Cannot create visualizations for incomplete reports', 'warning')
        return redirect(url_for('reports.view', report_id=report.id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        visualization_type = request.form.get('visualization_type')
        
        # Basic configuration based on visualization type
        configuration = {
            'type': visualization_type,
            'data': {},
            'options': {}
        }
        
        visualization = Visualization(
            report_id=report.id,
            title=title,
            description=description,
            visualization_type=visualization_type,
            configuration=configuration
        )
        
        db.session.add(visualization)
        db.session.commit()
        
        flash('Visualization added successfully', 'success')
        return redirect(url_for('reports.view', report_id=report.id))
    
    return render_template('reports/create_visualization.html', report=report)

@reports_bp.route('/api/update-status/<int:report_id>', methods=['POST'])
@login_required
def update_status(report_id):
    """Update report status (API endpoint for agents)."""
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    
    data = request.json
    status = data.get('status')
    report_data = data.get('data')
    
    if status == 'completed':
        report.complete(report_data)
    elif status == 'error':
        error_message = data.get('error_message', 'Unknown error')
        report.mark_error(error_message)
    else:
        report.status = status
        db.session.commit()
    
    return jsonify({'success': True}) 