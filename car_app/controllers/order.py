from flask import Blueprint, request, jsonify
from car_app.Models.order import Order
from car_app.Models.car import Car
from car_app.Models.user import User
from car_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Create a Blueprint for order endpoints
order_blueprint = Blueprint('order', __name__, url_prefix='/api/v1/orders')

# Define the create order endpoint
@order_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        car_id = data.get('carId')

        # Validate required fields
        if not car_id:
            return jsonify({'error': 'Car ID is required'}), 400

        # Check if the car exists
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404

        # Create a new order object
        new_order = Order(
            car_id=car_id,
            user_id=current_user_id
        )

        # Add new order to the database
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully', 'orderId': new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the get order endpoint
@order_blueprint.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        serialized_order = {
            'id': order.id,
            'car_id': order.car_id,
            'user_id': order.user_id,
            'created_at': order.created_at.isoformat(),
            'status': order.status,
            'payment_status': order.payment_status,
            'payment_method': order.payment_method,
            'transaction_id': order.transaction_id,
            'payment_date': order.payment_date.isoformat() if order.payment_date else None
        }

        return jsonify({'order': serialized_order}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get all orders endpoint
@order_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_orders():
    try:
        orders = Order.query.all()
        serialized_orders = [{
            'id': order.id,
            'car_id': order.car_id,
            'user_id': order.user_id,
            'created_at': order.created_at.isoformat(),
            'status': order.status,
            'payment_status': order.payment_status,
            'payment_method': order.payment_method,
            'transaction_id': order.transaction_id,
            'payment_date': order.payment_date.isoformat() if order.payment_date else None
        } for order in orders]

        return jsonify({'orders': serialized_orders}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the update order endpoint
@order_blueprint.route('/update/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Check if the current user is authorized to update the order
        if order.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Update order fields if provided in request
        order.status = data.get('status', order.status)
        order.payment_status = data.get('paymentStatus', order.payment_status)
        order.payment_method = data.get('paymentMethod', order.payment_method)
        order.transaction_id = data.get('transactionId', order.transaction_id)
        order.payment_date = datetime.fromisoformat(data.get('paymentDate')) if data.get('paymentDate') else order.payment_date

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'Order updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the delete order endpoint
@order_blueprint.route('/delete/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Retrieve order by ID
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Check if the current user is authorized to delete the order
        if order.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete order from database
        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
