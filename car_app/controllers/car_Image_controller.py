from flask import Blueprint, request, jsonify
from car_app.Models.car_Image import CarImage
from car_app.Models.car import Car
from car_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity


# Create a Blueprint for car image endpoints
car_image_blueprint = Blueprint('car_image', __name__, url_prefix='/api/v1/car_images')



# Define the create car image endpoint
@car_image_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_car_image():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")  

        # Extract request data
        data = request.json
        car_id = data.get('car_id')
        image_path = data.get('image_path')
        print(f"Received data - Car ID: {car_id}, Image Path: {image_path}")  

        # Validate required fields
        if not car_id or not image_path:
            return jsonify({'error': 'Car ID and image path are required'}), 400

        # Check if the car exists and belongs to the current user
        car = Car.query.get(car_id)
        print(f"Queried Car: {car}")  

        if not car:
            return jsonify({'error': 'Car not found'}), 404
        if car.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Create a new car image object
        new_car_image = CarImage(car_id=car_id, image_path=image_path)

        # Add new car image to the database
        db.session.add(new_car_image)
        db.session.commit()

        return jsonify({'message': 'Car image created successfully', 'car_image': new_car_image.id}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")  
        return jsonify({'error': str(e)}), 500

# Define the get car image endpoint
@car_image_blueprint.route('/<int:image_id>', methods=['GET'])
def get_car_image(image_id):
    try:
        car_image = CarImage.query.get(image_id)
        if not car_image:
            return jsonify({'error': 'Car image not found'}), 404

        serialized_car_image = {
            'id': car_image.id,
            'car_id': car_image.car_id,
            'image_path': car_image.image_path
        }

        return jsonify({'car_image': serialized_car_image}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get all car images endpoint
@car_image_blueprint.route('/', methods=['GET'])
def get_all_car_images():
    try:
        car_images = CarImage.query.all()
        serialized_car_images = [{
            'id': car_image.id,
            'car_id': car_image.car_id,
            'image_path': car_image.image_path
        } for car_image in car_images]

        return jsonify({'car_images': serialized_car_images}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the update car image endpoint
@car_image_blueprint.route('/edit/<int:image_id>', methods=['PUT'])
@jwt_required()
def update_car_image(image_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")  

        # Extract request data
        data = request.json
        print(f"Received data: {data}")  

        # Retrieve car image from the database
        car_image = CarImage.query.get(image_id)
        if not car_image:
            print(f"Car image with ID {image_id} not found") 
            return jsonify({'error': 'Car image not found'}), 404

        # Check if the current user is the owner of the car associated with the image
        car = Car.query.get(car_image.car_id) 
        if car is None:
            print(f"Car with ID {car_image.car_id} not found")  
            return jsonify({'error': 'Car not found'}), 404

        if car.user_id != current_user_id:
            print(f"Unauthorized access by user ID {current_user_id} for car ID {car.id}")  
            return jsonify({'error': 'Unauthorized access'}), 403

        # Update car image fields if provided in request
        car_image.image_path = data.get('image_path', car_image.image_path)
        print(f"Updated image path: {car_image.image_path}")

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Car image updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Exception: {str(e)}")  
        return jsonify({'error': str(e)}), 500

# Define the delete car image endpoint
@car_image_blueprint.route('/delete/<int:image_id>', methods=['DELETE'])
@jwt_required()
def delete_car_image(image_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")

        # Retrieve car image from the database
        car_image = CarImage.query.get(image_id)
        if not car_image:
            print(f"Car image with ID {image_id} not found")  
            return jsonify({'error': 'Car image not found'}), 404

        # Check if the current user is the owner of the car associated with the image
        car = Car.query.get(car_image.car_id)
        if car is None:
            print(f"Car with ID {car_image.car_id} not found")  
            return jsonify({'error': 'Car not found'}), 404

        if car.user_id != current_user_id:
            print(f"Unauthorized access by user ID {current_user_id} for car ID {car.id}")  
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete the car image
        db.session.delete(car_image)
        db.session.commit()

        return jsonify({'message': 'Car image deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Exception: {str(e)}")  
        return jsonify({'error': str(e)}), 500
