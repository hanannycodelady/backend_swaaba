from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class LatestCar(db.Model):
    __tablename__ = 'latest_cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer, nullable=True)
    fuel_type = db.Column(db.String(50), nullable=True)
    body_type = db.Column(db.String(50), nullable=True)
    transmission = db.Column(db.String(50), nullable=True)
    condition = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically stores when the car was added
    
    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "mileage": self.mileage,
            "fuel_type": self.fuel_type,
            "body_type": self.body_type,
            "transmission": self.transmission,
            "condition": self.condition,
            "color": self.color,
            "date_added": self.date_added
        }
