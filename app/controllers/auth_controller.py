from flask import Blueprint, request, jsonify, make_response
from app.services.auth_service import AuthService
from app.models.user import User
from werkzeug.security import check_password_hash 
from flask import current_app
from bson import json_util

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User(current_app).get_user_by_email(data['email'])
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # Remove the password field
    user.pop('password', None)
    user_json = json_util.dumps(user)

    mongo_uri = current_app.config['MONGO_URI']
    auth_token = AuthService.encode_auth_token(user['_id'], mongo_uri)
    return jsonify({'user': user_json, 'token': auth_token}), 200

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Name, email, and password are required'}), 400

    existing_user = User(current_app).get_user_by_email(data['email'])
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    User.create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user'),
        phone=data.get('phone', '')
    )

    return jsonify({'message': 'User registered successfully'}), 201
