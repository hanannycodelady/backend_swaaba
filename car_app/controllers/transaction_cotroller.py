from flask import Blueprint, request, jsonify
from car_app.Models.transactions import Transaction, db
from car_app.Models.car import Car
from car_app.Models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Create a Blueprint for transaction endpoints
transaction = Blueprint('transaction', __name__, url_prefix='/api/v1/transaction')

# Define the create transaction endpoint
@transaction.route('/create', methods=['POST'])
@jwt_required()
def create_transaction():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        car_id = data.get('car_id')
        amount = data.get('amount')

        # Validate required fields
        if not car_id or not amount:
            return jsonify({'error': 'Car ID and amount are required'}), 400

        # Validate car existence
        car = Car.query.get(car_id)
        if not car:
            return jsonify({'error': 'Car not found'}), 404

        # Validate current user is not the owner of the car
        if car.user_id == current_user_id:
            return jsonify({'error': 'You cannot buy your own car'}), 403

        # Create a new transaction object
        new_transaction = Transaction(
            car_id=car_id,
            buyer_id=current_user_id,
            seller_id=car.user_id,
            date=datetime.utcnow(),
            amount=amount
        )

        # Add new transaction to the database
        db.session.add(new_transaction) 
        db.session.commit()

        return jsonify({'message': 'Transaction created successfully', 'transaction': new_transaction.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the get transaction endpoint
@transaction.route('/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        serialized_transaction = {
            'id': transaction.id,
            'car_id': transaction.car_id,
            'buyer_id': transaction.buyer_id,
            'seller_id': transaction.seller_id,
            'date': transaction.date,
            'amount': str(transaction.amount)
        }

        return jsonify({'transaction': serialized_transaction}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get all transactions endpoint
@transaction.route('/', methods=['GET'])
def get_all_transactions():
    try:
        transactions = Transaction.query.all()
        serialized_transactions = [{
            'id': transaction.id,
            'car_id': transaction.car_id,
            'buyer_id': transaction.buyer_id,
            'seller_id': transaction.seller_id,
            'date': transaction.date,
            'amount': str(transaction.amount)
        } for transaction in transactions]

        return jsonify({'transactions': serialized_transactions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get transactions by user endpoint
@transaction.route('/user/<int:user_id>', methods=['GET'])
def get_transactions_by_user(user_id):
    try:
        transactions = Transaction.query.filter((Transaction.buyer_id == user_id) | (Transaction.seller_id == user_id)).all()
        serialized_transactions = [{
            'id': transaction.id,
            'car_id': transaction.car_id,
            'buyer_id': transaction.buyer_id,
            'seller_id': transaction.seller_id,
            'date': transaction.date,
            'amount': str(transaction.amount)
        } for transaction in transactions]

        return jsonify({'transactions': serialized_transactions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the update transaction endpoint
@transaction.route('/edit/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        # Check if the current user is involved in the transaction
        if transaction.buyer_id != current_user_id and transaction.seller_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Update transaction fields if provided in request
        transaction.amount = data.get('amount', transaction.amount)

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'Transaction updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the delete transaction endpoint
@transaction.route('/delete/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Retrieve transaction by ID
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        # Check if the current user is involved in the transaction
        if transaction.buyer_id != current_user_id and transaction.seller_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete transaction from database
        db.session.delete(transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500