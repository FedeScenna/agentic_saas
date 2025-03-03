import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Agent, DataSource, Subscription

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/')
@login_required
def index():
    """Render the agents list page."""
    agents = Agent.query.filter_by(user_id=current_user.id).all()
    return render_template('agents/index.html', agents=agents)

@agents_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Handle agent creation."""
    # Check subscription limits
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    if not subscription or not subscription.is_active:
        flash('You need an active subscription to create agents', 'warning')
        return redirect(url_for('subscription.plans'))
    
    # Check agent count based on subscription plan
    agent_count = Agent.query.filter_by(user_id=current_user.id).count()
    max_agents = 1  # Default for basic plan
    
    if subscription.plan_type == 'professional':
        max_agents = 3
    elif subscription.plan_type == 'enterprise':
        max_agents = 999  # Effectively unlimited
    
    if agent_count >= max_agents:
        flash(f'Your {subscription.plan_type.capitalize()} plan allows a maximum of {max_agents} agents', 'warning')
        return redirect(url_for('subscription.upgrade'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        # Generate a unique API key
        api_key = str(uuid.uuid4())
        
        agent = Agent(
            user_id=current_user.id,
            name=name,
            description=description,
            api_key=api_key,
            status='inactive',
            configuration={}
        )
        
        db.session.add(agent)
        db.session.commit()
        
        flash('Agent created successfully', 'success')
        return redirect(url_for('agents.view', agent_id=agent.id))
    
    return render_template('agents/create.html')

@agents_bp.route('/<int:agent_id>')
@login_required
def view(agent_id):
    """View agent details."""
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first_or_404()
    data_sources = DataSource.query.filter_by(agent_id=agent.id).all()
    
    return render_template('agents/view.html', agent=agent, data_sources=data_sources)

@agents_bp.route('/<int:agent_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(agent_id):
    """Edit agent details."""
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        agent.name = request.form.get('name')
        agent.description = request.form.get('description', '')
        
        db.session.commit()
        flash('Agent updated successfully', 'success')
        return redirect(url_for('agents.view', agent_id=agent.id))
    
    return render_template('agents/edit.html', agent=agent)

@agents_bp.route('/<int:agent_id>/delete', methods=['POST'])
@login_required
def delete(agent_id):
    """Delete an agent."""
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first_or_404()
    
    # Delete associated data sources
    DataSource.query.filter_by(agent_id=agent.id).delete()
    
    db.session.delete(agent)
    db.session.commit()
    
    flash('Agent deleted successfully', 'success')
    return redirect(url_for('agents.index'))

@agents_bp.route('/<int:agent_id>/toggle', methods=['POST'])
@login_required
def toggle(agent_id):
    """Toggle agent status (activate/deactivate)."""
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first_or_404()
    
    if agent.status == 'active':
        agent.deactivate()
        flash('Agent deactivated', 'info')
    else:
        agent.activate()
        flash('Agent activated', 'success')
    
    return redirect(url_for('agents.view', agent_id=agent.id))

@agents_bp.route('/<int:agent_id>/data-sources/create', methods=['GET', 'POST'])
@login_required
def create_data_source(agent_id):
    """Create a new data source for an agent."""
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        name = request.form.get('name')
        source_type = request.form.get('source_type')
        connection_string = request.form.get('connection_string', '')
        
        data_source = DataSource(
            agent_id=agent.id,
            name=name,
            source_type=source_type,
            connection_string=connection_string,
            is_active=True,
            configuration={}
        )
        
        db.session.add(data_source)
        db.session.commit()
        
        flash('Data source added successfully', 'success')
        return redirect(url_for('agents.view', agent_id=agent.id))
    
    return render_template('agents/create_data_source.html', agent=agent)

@agents_bp.route('/api/regenerate-key/<int:agent_id>', methods=['POST'])
@login_required
def regenerate_api_key(agent_id):
    """Regenerate the API key for an agent."""
    agent = Agent.query.filter_by(id=agent_id, user_id=current_user.id).first_or_404()
    
    # Generate a new API key
    agent.api_key = str(uuid.uuid4())
    db.session.commit()
    
    return jsonify({'success': True, 'api_key': agent.api_key}) 