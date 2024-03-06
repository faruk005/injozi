from flask import Flask
from flask_restful import Api
from config import Config
from flask_jwt_extended import JWTManager
# Import auth blueprint
from app.controllers.auth_controller import auth_bp  
from app.controllers.user_controller import user_bp 

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
jwt = JWTManager(app)

app.config.update({
    'JWT_TOKEN_LOCATION': ['headers'],
    'JWT_HEADER_NAME': 'Authorization',
    'JWT_HEADER_TYPE': 'Bearer',
    'JWT_ACCESS_COOKIE_NAME': 'access_token',
    'JWT_REFRESH_COOKIE_NAME': 'refresh_token',
    'JWT_COOKIE_CSRF_PROTECT': True,
    'JWT_CSRF_IN_COOKIES': True,
    'JWT_COOKIE_SECURE': False, 
    'JWT_COOKIE_SAMESITE': 'Lax', 
})


# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')


@app.route('/')
def index():
    return 'Hello, Flask app!'

if __name__ == '__main__':
    app.run(debug=True)
