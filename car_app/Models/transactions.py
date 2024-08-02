from car_app.extensions import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    car = db.relationship('Car', foreign_keys=[car_id], backref='transactions')
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='bought_transactions')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sold_transactions')

    def __init__(self, car_id, buyer_id, seller_id, date, amount):
        self.car_id = car_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.date = date
        self.amount = amount


