from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from flask import current_app as app

# client = MongoClient(app.config['MONGO_URI'])
# db = client.get_database()

class User:
    #collection = None 
    
    def __init__(self, app):
        self.app = app
        self.client = MongoClient(app.config['MONGO_URI'])
        self.db = self.client.get_database()
        self.collection = self.db.users
        User.collection = self.collection
     
    # save user details on update  
    def save_user(self, user_data):
        user_id = user_data.pop('_id')  # Remove _id field temporarily
        self.collection.update_one({'_id': user_id}, {'$set': user_data})
        user_data['_id'] = user_id

    # create a new user
    @staticmethod
    def create_user(name, email, password, role, phone):
        hashed_password = generate_password_hash(password)
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password, #hash password once
            'role': role,
            'phone': phone
        }
        User.collection.insert_one(user_data)

    # @staticmethod
    # def get_user_by_email(email):
    #     return User.collection.find_one({'email': email})
    
    # return user by email
    @classmethod
    def get_user_by_email(cls, email):  # Use classmethod decorator
        return cls.collection.find_one({'email': email})
    
    # return user by id
    @classmethod
    def get_user_by_id(cls,user_id):
        user_data = cls.collection.find_one({'_id': ObjectId(user_id)})
        # return user_data
        if user_data:
                return user_data
        else:
            return None
    
    # return all user
    @classmethod
    def get_all_users(cls):
        users_data = cls.collection.find({})
        return list(users_data)
        
