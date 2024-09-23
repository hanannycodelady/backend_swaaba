import os
from flask import current_app, Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from car_app.Models.car_Image import CarImage
from car_app.Models.car import Car
from car_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Create a Blueprint for car image endpoints
car_image_blueprint = Blueprint('car_image', __name__, url_prefix='/api/v1/car_images')

@car_image_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_car_image():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Get form data and file
        car_id = request.form.get('car_id')
        image_file = request.files.get('image')

        # Validate required fields
        if not car_id or not image_file:
            return jsonify({'error': 'Car ID and image file are required'}), 400

        # Check if the car exists and belongs to the current user
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404
        if car.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Check if file is allowed
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Secure the filename and save it to the upload folder
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)

        # Create a new car image object with the relative path
        new_car_image = CarImage(car_id=car_id, image_path=filename)

        # Add new car image to the database
        db.session.add(new_car_image)
        db.session.commit()

        return jsonify({'message': 'Car image uploaded successfully', 'car_image': new_car_image.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@car_image_blueprint.route('/<int:image_id>', methods=['GET'])
def get_car_image(image_id):
    try:
        car_image = CarImage.query.get(image_id)
        if not car_image:
            return jsonify({'error': 'Car image not found'}), 404

        image_url = f"/uploaded_images/{car_image.image_path}"
        serialized_car_image = {
            'id': car_image.id,
            'car_id': car_image.car_id,
            'image_url': image_url
        }

        return jsonify({'car_image': serialized_car_image}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
