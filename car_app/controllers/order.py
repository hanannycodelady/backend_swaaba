from flask import Blueprint, request, jsonify, current_app as app
from car_app.Models.order import Order
from car_app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Create a Blueprint for order and payment endpoints
order_blueprint = Blueprint('order', __name__, url_prefix='/api/v1/orders')

# Create an order
@order_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    try:
        current_user_id = get_jwt_identity()

        data = request.json.get('order', {})
        car_id = data.get('car_id')
        payment_method = data.get('payment_method')
        card_number = data.get('card_number')
        payment_date_str = data.get('payment_date')

        if not car_id or not payment_method:
            return jsonify({'error': 'Car ID and Payment Method are required'}), 400

        # Validate and parse the payment_date
        payment_date = None
        if payment_date_str:
            try:
                payment_date = datetime.fromisoformat(payment_date_str)
            except ValueError:
                return jsonify({'error': 'Invalid payment date format'}), 400

        # Create the Order object
        order = Order(
            car_id=car_id,
            payment_method=payment_method,
            payment_date=payment_date,
            card_number=card_number,
        )

        db.session.add(order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully', 'order_id': order.id}), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error creating order: {e}')
        return jsonify({'error': 'An error occurred while creating the order.'}), 500

# Get order by ID
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
            'payment_method': order.payment_method,
            'payment_date': order.payment_date.isoformat() if order.payment_date else None,
            'card_number': order.card_number,
            'created_at': order.created_at.isoformat() if order.created_at else None
        }

        return jsonify({'order': serialized_order}), 200

    except Exception as e:
        app.logger.error(f'Error retrieving order: {e}')
        return jsonify({'error': 'An error occurred while retrieving the order.'}), 500

# Get all orders
@order_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_orders():
    try:
        orders = Order.query.all()
        serialized_orders = [{
            'id': order.id,
            'car_id': order.car_id,
            'payment_method': order.payment_method,
            'payment_date': order.payment_date.isoformat() if order.payment_date else None,
            'card_number': order.card_number,
            'created_at': order.created_at.isoformat() if order.created_at else None
        } for order in orders]

        return jsonify({'orders': serialized_orders}), 200

    except Exception as e:
        app.logger.error(f'Error retrieving orders: {e}')
        return jsonify({'error': 'An error occurred while retrieving the orders.'}), 500

# Update an order
@order_blueprint.route('/edit/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    try:
        data = request.json.get('order', {})
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.payment_method = data.get('payment_method', order.payment_method)
        order.card_number = data.get('card_number', order.card_number)

        db.session.commit() 

        return jsonify({'message': 'Order updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating order: {e}')
        return jsonify({'error': 'An error occurred while updating the order.'}), 500

# Delete an order
@order_blueprint.route('/delete/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting order: {e}')
        return jsonify({'error': 'An error occurred while deleting the order.'}), 500
