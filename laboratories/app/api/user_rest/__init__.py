from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .controller import UserRestController, UserListRestController

user_rest_bp = Blueprint('user_rest_bp', __name__)
api = Api(user_rest_bp, errors=user_rest_bp.app_errorhandler)

api.add_resource(UserRestController, '', '/', '/<int:id>')
api.add_resource(UserListRestController, '/list')


@user_rest_bp.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
