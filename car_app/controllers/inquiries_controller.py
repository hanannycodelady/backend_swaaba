from flask import Blueprint, request, jsonify, abort
from car_app.extensions import db
from car_app.Models.inquiry import Inquiry
from car_app.Models.car import Car
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for inquiry endpoints
inquiry_blueprint = Blueprint('inquiry', __name__, url_prefix='/api/v1/inquiries')

# Create a new inquiry
@inquiry_blueprint.route('/create', methods=['POST'])
@jwt_required()  
def create_inquiry():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        car_id = data.get('car_id')
        name = data.get('name')
        email = data.get('email')
        telephone = data.get('telephone')
        message = data.get('message')

        # Validate required fields
        required_fields = ['car_id', 'name', 'email', 'telephone', 'message']
        if not all(data.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if car_id exists in the car table
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Invalid car ID'}), 400

        # Create a new inquiry object
        new_inquiry = Inquiry(
            car_id=car_id,
            name=name,
            email=email,
            telephone=telephone,
            message=message
        )

        # Add new inquiry to the database
        db.session.add(new_inquiry)
        db.session.commit()

        return jsonify({'message': 'Inquiry created successfully', 'inquiry': new_inquiry.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all inquiries
@inquiry_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_inquiries():
    try:
        inquiries = Inquiry.query.all()
        inquiries_list = [
            {
                "id": inquiry.id,
                "car_id": inquiry.car_id,
                "name": inquiry.name,
                "email": inquiry.email,
                "telephone": inquiry.telephone,
                "message": inquiry.message,
                "created_at": inquiry.created_at
            } for inquiry in inquiries
        ]
        return jsonify({'inquiries': inquiries_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a specific inquiry by ID
@inquiry_blueprint.route('/<int:inquiry_id>', methods=['GET'])
@jwt_required()
def get_inquiry(inquiry_id):
    try:
        inquiry = Inquiry.query.get(inquiry_id)
        if not inquiry:
            return jsonify({'error': 'Inquiry not found'}), 404

        inquiry_data = {
            "id": inquiry.id,
            "car_id": inquiry.car_id,
            "name": inquiry.name,
            "email": inquiry.email,
            "telephone": inquiry.telephone,
            "message": inquiry.message,
            "created_at": inquiry.created_at
        }
        return jsonify({'inquiry': inquiry_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an existing inquiry
@inquiry_blueprint.route('/edit/<int:inquiry_id>', methods=['PUT'])
@jwt_required()
def update_inquiry(inquiry_id):
    try:
        # Extract request data
        data = request.json
        inquiry = Inquiry.query.get(inquiry_id)
        if not inquiry:
            return jsonify({'error': 'Inquiry not found'}), 404

        # Update inquiry fields if provided in request
        inquiry.car_id = data.get('car_id', inquiry.car_id)
        inquiry.name = data.get('name', inquiry.name)
        inquiry.email = data.get('email', inquiry.email)
        inquiry.telephone = data.get('telephone', inquiry.telephone)
        inquiry.message = data.get('message', inquiry.message)

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'Inquiry updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an inquiry
@inquiry_blueprint.route('/delete/<int:inquiry_id>', methods=['DELETE'])
@jwt_required()
def delete_inquiry(inquiry_id):
    try:
        inquiry = Inquiry.query.get(inquiry_id)
        if not inquiry:
            return jsonify({'error': 'Inquiry not found'}), 404

        # Delete inquiry from database
        db.session.delete(inquiry)
        db.session.commit()

        return jsonify({'message': 'Inquiry deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
