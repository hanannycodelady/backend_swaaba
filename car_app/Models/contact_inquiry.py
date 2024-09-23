from sqlalchemy.orm import relationship
from car_app.extensions import db
from datetime import datetime

class Contact_inquiry(db.Model):
    __tablename__ = 'contacts_inquiry'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    car_id = db.Column(db.Integer, nullable=True)  
    phone_number = db.Column(db.String(20), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    def __init__(self, user_id, username, email, message, car_id=None, phone_number=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.message = message
        self.car_id = car_id  # Initialize car_id
        self.phone_number = phone_number  # Initialize phone_number
    
    def __repr__(self):
        return (f'<Contact {self.id} - Car ID: {self.car_id} - Phone Number: {self.phone_number}>')
