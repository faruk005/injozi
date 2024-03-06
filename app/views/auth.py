from flask import Blueprint
from controllers.auth_controller import auth_bp

# Register routes
auth_routes = Blueprint('auth_routes', __name__)
auth_routes.register_blueprint(auth_bp)
