from datetime import datetime
from car_app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False) 
    payment_method = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=True)
    card_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    car = db.relationship('Car', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.id} for Car {self.car_id} with {self.payment_method}>'
