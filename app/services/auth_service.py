from flask import current_app as app
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

#client = MongoClient(app.config['MONGO_URI'])
#db = client.get_database()

class AuthService:
    def __init__(self, app):
        self.app = app
        self.client = MongoClient(app.config['MONGO_URI'])
        
    @staticmethod
    def encode_auth_token(user_id, mongo_uri):
        try:
            client = MongoClient(mongo_uri)
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': str(user_id)  # Ensure user_id is converted to string
            }
            return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
