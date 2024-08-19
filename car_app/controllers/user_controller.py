
# Import necessary modules
from flask import Blueprint, request, jsonify
from car_app.Models.user import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity 
from flask_jwt_extended import JWTManager

# Create a Blueprint for authentication endpoints
user = Blueprint('user', __name__, url_prefix='/api/v1/user')

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize JWTManager
jwt = JWTManager()

# Define the registration endpoint
@user.route('/register', methods=['POST'])
def register():
    try:
        # Extract request data
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        contact = data.get('contact')
        email = data.get('email')
        password = data.get('password')
        avatar_url = data.get('avatar_url', "https://cdn-icons-png.flaticon.com/128/17588/17588241.png")  # Default avatar URL

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'contact', 'password', 'email']
        if not all(data.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password is too short'}), 400

        # Check if email and contact already exist
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error': 'Email already exists'}), 409
        if User.query.filter_by(contact=contact).first() is not None:
            return jsonify({'error': 'Contact already exists'}), 409

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user object
        new_user = User(first_name=first_name, last_name=last_name, email=email, contact=contact, password=hashed_password, avatar_url=avatar_url)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Construct response
        username = f"{new_user.first_name} {new_user.last_name}"
        return jsonify({
            'message': f'{username} has been successfully created',
            'user': {
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'contact': new_user.contact,
                'avatar_url': new_user.avatar_url,
                'created_at': new_user.created_at,
            } 
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the login endpoint
@user.route('/login', methods=["POST"])
def login():
    try:
        # Extract request data
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Check if the user has an avatar set; if not, provide a default avatar
            # Set default avatar
            avatar_url = user.avatar_url or "https://cdn-icons-png.flaticon.com/128/17588/17588241.png"

            # Create access token
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'access_token': access_token,
                'user_id': user.id,
                'user_name': f"{user.first_name} {user.last_name}",
                'avatar_url': avatar_url  # Return the avatar URL
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the edit user endpoint
@user.route('/edit/<int:user_id>', methods=["PUT"])
@jwt_required()
def edit_user(user_id):
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Extract request data
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update user fields if provided in request
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.contact = data.get('contact', user.contact)
        
        # Update password if provided
        password = data.get('password')
        if password:
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Commit changes to database
        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the delete user endpoint
@user.route('/delete/<int:user_id>', methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # Retrieve user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Delete user from database
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the get specific user endpoint
@user.route('/user/<int:user_id>', methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)

        if user:
            serialized_user = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'contact': user.contact
            }
            return jsonify({'user': serialized_user}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the endpoint to get all users
@user  .route('/users', methods=['GET'])
def get_all_users():
    try:
        # Retrieve all users from the database
        users = User.query.all()

        # Serialize the users' data into a list of dictionaries
        serialized_users = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact': user.contact
        } for user in users]

        # Return the list of serialized users in a JSON response
        return jsonify({'users': serialized_users}), 200

    except Exception as e:
        # If an exception occurs, return a server error response
        return jsonify({'error': str(e)}), 500

