from flask import Blueprint, request, jsonify
from car_app.Models.review import Review, db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for review endpoints
review_blueprint = Blueprint('review', __name__, url_prefix='/api/v1/reviews')

# Define the create review endpoint
@review_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_review():
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        car_id = data.get('car_id')
        rating = data.get('rating')
        comment = data.get('comment')

        # Validate required fields
        if not car_id or not rating:
            return jsonify({'error': 'Car ID and rating are required'}), 400

        # Create a new review object
        new_review = Review(user_id=current_user_id, car_id=car_id, rating=rating, comment=comment)

        # Add new review to the database
        db.session.add(new_review)
        db.session.commit()

        return jsonify({'message': 'Review created successfully', 'review': new_review.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the get review endpoint
@review_blueprint.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    try:
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404

        serialized_review = {
            'id': review.id,
            'user_id': review.user_id,
            'car_id': review.car_id,
            'rating': review.rating,
            'comment': review.comment
        }

        return jsonify({'review': serialized_review}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get all reviews endpoint
@review_blueprint.route('/', methods=['GET'])
def get_all_reviews():
    try:
        reviews = Review.query.all()
        serialized_reviews = [{
            'id': review.id,
            'user_id': review.user_id,
            'car_id': review.car_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]

        return jsonify({'reviews': serialized_reviews}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the get reviews by car endpoint
@review_blueprint.route('/car/<int:car_id>', methods=['GET'])
def get_reviews_by_car(car_id):
    try:
        reviews = Review.query.filter_by(car_id=car_id).all()
        serialized_reviews = [{
            'id': review.id,
            'user_id': review.user_id,
            'car_id': review.car_id,
            'rating': review.rating,
            'comment': review.comment
        } for review in reviews]

        return jsonify({'reviews': serialized_reviews}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the update review endpoint
@review_blueprint.route('/edit/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Extract request data
        data = request.json
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404

        # Check if the current user is the owner of the review
        if review.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Update review fields if provided in request
        review.rating = data.get('rating', review.rating)
        review.comment = data.get('comment', review.comment)

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'Review updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the delete review endpoint
@review_blueprint.route('/delete/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    try:
        # Get the current user ID from JWT
        current_user_id = get_jwt_identity()

        # Retrieve review by ID
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404

        # Check if the current user is the owner of the review
        if review.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete review from database
        db.session.delete(review)
        db.session.commit()

        return jsonify({'message': 'Review deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
 