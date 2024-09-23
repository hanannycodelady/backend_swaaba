from car_app import db

class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # New attributes
    engine = db.Column(db.String(100), nullable=False)
    steering = db.Column(db.String(50), nullable=False)
    mileage = db.Column(db.Float, nullable=False)  
    seats = db.Column(db.Integer, nullable=False)
    
    # New attributes
    fuel_type = db.Column(db.String(50), nullable=False)
    body_type = db.Column(db.String(50), nullable=False)
    transmission = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    images = db.relationship('CarImage', backref='car', lazy=True)  
    # reviews = db.relationship('Review', backref='car', lazy=True)
    # transactions = db.relationship('Transaction', backref='car', lazy=True)

    def __init__(self, make, model, year, price, description, engine, steering, mileage, seats, fuel_type, body_type, transmission, condition, color, user_id):
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.description = description
        self.engine = engine
        self.steering = steering
        self.mileage = mileage
        self.seats = seats
        self.fuel_type = fuel_type
        self.body_type = body_type
        self.transmission = transmission
        self.condition = condition
        self.color = color
        self.user_id = user_id
