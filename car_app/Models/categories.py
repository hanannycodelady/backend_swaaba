from car_app.extensions import db

class Make(db.Model):
    __tablename__ = 'make'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, name):
        self.name = name

class BodyType(db.Model):
    __tablename__ = 'body_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, type):
        self.type = type

class FuelType(db.Model):
    __tablename__ = 'fuel_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, type):
        self.type = type

class Transmission(db.Model):
    __tablename__ = 'transmission'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, type):
        self.type = type

class Condition(db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, condition):
        self.condition = condition

class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, color):
        self.color = color