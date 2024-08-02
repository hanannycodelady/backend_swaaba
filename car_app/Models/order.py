from car_app.extensions import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')  
    
    
    # Payment information
    payment_status = db.Column(db.String(20), default='Pending') 
    payment_method = db.Column(db.String(50))  
    transaction_id = db.Column(db.String(100))  
    payment_date = db.Column(db.DateTime)  
    
    car = db.relationship('Car', backref='orders', lazy=True)
    user = db.relationship('User', backref='orders', lazy=True)
