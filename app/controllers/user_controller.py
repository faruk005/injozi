from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from bson import json_util
from flask import current_app

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_details():
    current_user_id = get_jwt_identity()
    user = User(current_app).get_user_by_id(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Exclude the password field
    user.pop('password', None)
    user['_id'] = str(user['_id']) 
    return jsonify({'user': user}), 200

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def edit_user_details():
    current_user_id = get_jwt_identity()
    user = User(current_app).get_user_by_id(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    # Only allow editing specific fields (e.g., name, email, phone)
    allowed_fields = {'name', 'phone'}
    for key, value in data.items():
        if key in allowed_fields:
            user[key] = value
    
    updated_data = {key: value for key, value in data.items() if key in allowed_fields}
    updated_data['_id'] = user['_id']

    # Update the user's details
    User(current_app).save_user(updated_data)
    
    # Exclude the password field
    user.pop('password', None)
    
    user['_id'] = str(user['_id']) 
    return jsonify({'user': user}), 200

@user_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    current_user = User(current_app).get_user_by_id(current_user_id)
    if not current_user or current_user['role'] != 'superadmin':
        return jsonify({'message': 'Access denied'}), 403
    
    # Fetch all users
    users = User(current_app).get_all_users()
    
    # Exclude the password field from each user
    for user in users:
        user.pop('password', None)
    
    return jsonify({'users': json_util.dumps(users)}), 200
