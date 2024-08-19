from car_app.extensions import db
from datetime import datetime
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True, default="https://cdn-icons-png.flaticon.com/128/17588/17588241.png")  # Default avatar URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    # cars = db.relationship('Car', backref='owner', lazy=True)
    # reviews = db.relationship('Review', backref='reviewer', lazy=True)
    # bought_transactions = db.relationship('Transaction', backref='buyer_user', foreign_keys='Transaction.buyer_id', lazy=True)
    # sold_transactions = db.relationship('Transaction', backref='seller_user', foreign_keys='Transaction.seller_id', lazy=True)

    
    def __init__(self, first_name, last_name, email, contact, password=None, avatar_url=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.avatar_url = avatar_url
        
        



