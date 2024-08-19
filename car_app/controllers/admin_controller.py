from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from car_app.Models.user import User

admin_blueprint = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


@admin_blueprint.route('/dashboard', methods=['GET'])
@jwt_required()
def access_dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user and user.is_admin:
        return jsonify({'message': 'Welcome to the admin dashboard'})
    else:
        return jsonify({'error': 'Access denied'}), 403
    


@admin_blueprint.route('/check', methods=['GET'])
@jwt_required()
def check_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user and user.is_admin:
        return jsonify({'is_admin': True})
    else:
        return jsonify({'is_admin': False})

