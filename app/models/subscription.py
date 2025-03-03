from datetime import datetime
from app import db

class Subscription(db.Model):
    """Subscription model for user subscription plans."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_type = db.Column(db.String(20), nullable=False)  # basic, professional, enterprise
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    payment_method = db.Column(db.String(50), nullable=True)
    last_payment_date = db.Column(db.DateTime, nullable=True)
    next_payment_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Subscription {self.plan_type} for User {self.user_id}>'
    
    @property
    def is_expired(self):
        """Check if the subscription has expired."""
        if not self.end_date:
            return False
        return datetime.utcnow() > self.end_date
    
    @property
    def days_remaining(self):
        """Calculate the number of days remaining in the subscription."""
        if not self.end_date or not self.is_active:
            return 0
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)
    
    def cancel(self):
        """Cancel the subscription."""
        self.is_active = False
        db.session.commit()
    
    def renew(self, days=30):
        """Renew the subscription for a specified number of days."""
        if self.end_date:
            self.end_date = max(self.end_date, datetime.utcnow())
        else:
            self.end_date = datetime.utcnow()
        
        # Add days to the end date
        from datetime import timedelta
        self.end_date += timedelta(days=days)
        
        self.is_active = True
        db.session.commit() 