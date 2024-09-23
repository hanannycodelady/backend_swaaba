from flask import Blueprint, request, jsonify
from car_app.Models.car import Car
from car_app.Models.car_Image import CarImage
from car_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

## Create a Blueprint for car endpoints
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
        engine = data.get('engine')
        steering = data.get('steering')
        mileage = data.get('mileage')
        seats = data.get('seats')
        fuel_type = data.get('fuel_type')
        body_type = data.get('body_type')
        transmission = data.get('transmission')
        condition = data.get('condition')
        color = data.get('color')
        images = data.get('images')

        # Validate required fields
        required_fields = ['make', 'model', 'year', 'price', 'engine', 'steering', 'mileage', 'seats', 'fuel_type', 'body_type', 'transmission', 'condition', 'color']
        if not all(data.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        # Create a new car object
        new_car = Car(
            make=make,
            model=model,
            year=year,
            price=price,
            description=description,
            engine=engine,
            steering=steering,
            mileage=mileage,
            seats=seats,
            fuel_type=fuel_type,
            body_type=body_type,
            transmission=transmission,
            condition=condition,
            color=color,
            user_id=current_user_id
        )

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
    
    # Get all cars endpoint
@car_blueprint.route('/all', methods=['GET'])
def get_all_cars():
    try:
        cars = Car.query.all()
        
        # Serialize the car data along with their images
        serialized_cars = [{
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': str(car.price),
            'description': car.description,
            'engine': car.engine,
            'steering': car.steering,
            'mileage': car.mileage,
            'seats': car.seats,
            'fuel_type': car.fuel_type,
            'body_type': car.body_type,
            'transmission': car.transmission,
            'condition': car.condition,
            'color': car.color,
            'images': [image.image_path for image in car.images]  # Include associated image paths
        } for car in cars]
        
        return jsonify({'cars': serialized_cars}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get a specific car by ID endpoint
@car_blueprint.route('/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    try:
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404

        # Serialize the car data along with its images
        serialized_car = {
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': str(car.price),
            'description': car.description,
            'engine': car.engine,
            'steering': car.steering,
            'mileage': car.mileage,
            'seats': car.seats,
            'fuel_type': car.fuel_type,
            'body_type': car.body_type,
            'transmission': car.transmission,
            'condition': car.condition,
            'color': car.color,
            'images': [image.image_path for image in car.images]  # Include associated image paths
        }
        
        return jsonify({'car': serialized_car}), 200

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
        car.engine = data.get('engine', car.engine)
        car.steering = data.get('steering', car.steering)
        car.mileage = data.get('mileage', car.mileage)
        car.seats = data.get('seats', car.seats)
        car.fuel_type = data.get('fuel_type', car.fuel_type)
        car.body_type = data.get('body_type', car.body_type)
        car.transmission = data.get('transmission', car.transmission)
        car.condition = data.get('condition', car.condition)
        car.color = data.get('color', car.color)

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
    # searching endpoint
@car_blueprint.route('/search', methods=['GET'])
def search_cars():
    try:
        query_params = request.args
        search_query = query_params.get('query', '')  # Combined search term
        min_price = query_params.get('min_price')
        max_price = query_params.get('max_price')
        engine = query_params.get('engine')
        steering = query_params.get('steering')

        # Start with the base Car query
        query = Car.query

        # If the combined search query is present, apply it to multiple fields
        if search_query:
            query = query.filter(
                (Car.make.ilike(f'%{search_query}%')) | 
                (Car.model.ilike(f'%{search_query}%')) |
                (Car.year.ilike(f'%{search_query}%'))
            )

        # Apply price filtering if provided
        if min_price:
            query = query.filter(Car.price >= float(min_price))
        if max_price:
            query = query.filter(Car.price <= float(max_price))

        # Apply additional filters for engine and steering
        if engine:
            query = query.filter(Car.engine.ilike(f'%{engine}%'))
        if steering:
            query = query.filter(Car.steering.ilike(f'%{steering}%'))

        # Execute the query and serialize the results
        cars = query.all()
        serialized_cars = [{
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'price': str(car.price)
        } for car in cars]
        
        # Return the filtered car results as a JSON response
        return jsonify({'cars': serialized_cars}), 200

    except Exception as e:
        # Handle any exceptions and return a 500 error
        return jsonify({'error': str(e)}), 500
