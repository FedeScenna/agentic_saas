from datetime import datetime
from app import db

class Report(db.Model):
    """Report model for data analysis reports."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    report_type = db.Column(db.String(20), nullable=False)  # analysis, summary, visualization
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, error
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    data = db.Column(db.JSON, nullable=True)
    
    # Relationships
    visualizations = db.relationship('Visualization', backref='report', lazy='dynamic')
    
    def __repr__(self):
        return f'<Report {self.title}>'
    
    @property
    def is_completed(self):
        """Check if the report is completed."""
        return self.status == 'completed'
    
    def complete(self, report_data=None):
        """Mark the report as completed."""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        if report_data:
            self.data = report_data
        db.session.commit()
    
    def mark_error(self, error_message=None):
        """Mark the report as having an error."""
        self.status = 'error'
        if error_message and isinstance(self.data, dict):
            if 'errors' not in self.data:
                self.data = {'errors': []}
            self.data['errors'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'message': error_message
            })
        db.session.commit()


class Visualization(db.Model):
    """Visualization model for report visualizations."""
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    visualization_type = db.Column(db.String(20), nullable=False)  # chart, graph, table
    configuration = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Visualization {self.title} for Report {self.report_id}>' 