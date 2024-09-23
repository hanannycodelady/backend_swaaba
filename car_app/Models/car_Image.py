from car_app import db
import os

class CarImage(db.Model):
    __tablename__ = 'car_image'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

    def __init__(self, car_id, image_path):
        self.car_id = car_id
        self.image_path = image_path
