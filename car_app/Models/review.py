from car_app.extensions import db

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    
    def __init__(self, user_id, car_id, rating, comment=None):
        self.user_id = user_id
        self.car_id = car_id
        self.rating = rating
        self.comment = comment

