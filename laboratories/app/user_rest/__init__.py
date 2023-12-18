from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .controller import UserRestController, UserListRestController

user_rest_bp = Blueprint('user_rest_bp', __name__)
api = Api(user_rest_bp, errors=user_rest_bp.errorhandler)

api.add_resource(UserRestController, '/api/user', '/api/user/<int:id>')
api.add_resource(UserListRestController, '/api/user/list')


@user_rest_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
