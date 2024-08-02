from car_app import db

class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    images = db.relationship('CarImage', backref='car', lazy=True)  
    # reviews = db.relationship('Review', backref='car', lazy=True)
    # transactions = db.relationship('Transaction', backref='car', lazy=True)

    def __init__(self, make, model, year, price, description, user_id):
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.description = description
        self.user_id = user_id


