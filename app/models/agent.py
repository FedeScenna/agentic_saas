from datetime import datetime
from app import db

class Agent(db.Model):
    """Agent model for local data analysis agents."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='inactive')  # inactive, active, error
    api_key = db.Column(db.String(64), unique=True, nullable=False)
    last_active = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    configuration = db.Column(db.JSON, nullable=True)
    
    # Relationships
    reports = db.relationship('Report', backref='agent', lazy='dynamic')
    data_sources = db.relationship('DataSource', backref='agent', lazy='dynamic')
    
    def __repr__(self):
        return f'<Agent {self.name}>'
    
    @property
    def is_active(self):
        """Check if the agent is currently active."""
        return self.status == 'active'
    
    def activate(self):
        """Activate the agent."""
        self.status = 'active'
        self.last_active = datetime.utcnow()
        db.session.commit()
    
    def deactivate(self):
        """Deactivate the agent."""
        self.status = 'inactive'
        db.session.commit()
    
    def report_error(self, error_message=None):
        """Report an error with the agent."""
        self.status = 'error'
        if error_message and isinstance(self.configuration, dict):
            if 'errors' not in self.configuration:
                self.configuration['errors'] = []
            self.configuration['errors'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'message': error_message
            })
        db.session.commit()


class DataSource(db.Model):
    """DataSource model for agent data sources."""
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    source_type = db.Column(db.String(20), nullable=False)  # database, file, api
    connection_string = db.Column(db.Text, nullable=True)
    credentials = db.Column(db.JSON, nullable=True)
    configuration = db.Column(db.JSON, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_sync = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<DataSource {self.name} for Agent {self.agent_id}>' 