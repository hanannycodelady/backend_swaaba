from flask import Blueprint, request, jsonify
from car_app.Models.car import Car
from car_app.Models.car_Image import CarImage
from car_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for car endpoints
car_blueprint = Blueprint('car', __name__, url_prefix='/api/v1/cars')

# Define the create car endpoint
@car_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_car():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        price = data.get('price')
        description = data.get('description')
        images = data.get('images')

        # Validate required fields
        required_fields = ['make', 'model', 'year', 'price']
        if not all(data.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        # Create a new car object
        new_car = Car(make=make, model=model, year=year, price=price, description=description, user_id=current_user_id)

        # Add new car to the database
        db.session.add(new_car)
        db.session.commit()

        # Add images to the database
        for image_path in images:
            new_image = CarImage(image_path=image_path, car_id=new_car.id)
            db.session.add(new_image)

        db.session.commit()

        return jsonify({'message': 'Car created successfully', 'car': new_car.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the get car endpoint
@car_blueprint.route('/<int:car_id>', methods=['GET'])
def get_car(car_id):
    try:
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404

        serialized_car = {
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': str(car.price),
            'description': car.description,
            'user_id': car.user_id,
            'images': [{'id': img.id, 'path': img.image_path} for img in car.images]
        }

        return jsonify({'car': serialized_car}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get all cars endpoint
@car_blueprint.route('/', methods=['GET'])
def get_all_cars():
    try:
        cars = Car.query.all()
        serialized_cars = [{
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': str(car.price),
            'description': car.description,
            'user_id': car.user_id,
            'images': [{'id': img.id, 'path': img.image_path} for img in car.images]
        } for car in cars]

        return jsonify({'cars': serialized_cars}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get cars by user endpoint
@car_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_cars_by_user(user_id):
    try:
        cars = Car.query.filter_by(user_id=user_id).all()
        serialized_cars = [{
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': str(car.price),
            'description': car.description,
            'user_id': car.user_id,
            'images': [{'id': img.id, 'path': img.image_path} for img in car.images]
        } for car in cars]

        return jsonify({'cars': serialized_cars}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the update car endpoint
@car_blueprint.route('/edit/<int:car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404

        # Check if the current user is the owner of the car
        if car.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Update car fields if provided in request
        car.make = data.get('make', car.make)
        car.model = data.get('model', car.model)
        car.year = data.get('year', car.year)
        car.price = data.get('price', car.price)
        car.description = data.get('description', car.description)

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'Car updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the delete car endpoint
@car_blueprint.route('/delete/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Retrieve car by ID
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404

        # Check if the current user is the owner of the car
        if car.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete car from database
        db.session.delete(car)
        db.session.commit()

        return jsonify({'message': 'Car deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500