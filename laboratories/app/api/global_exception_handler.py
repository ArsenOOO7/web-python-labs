from flask import jsonify

from app.api import api
from app.util.exceptions import AccessTokenException, EntityNotFoundException


@api.app_errorhandler(AccessTokenException)
def access_token_exception(e: AccessTokenException):
    return jsonify({'message': e.message}), e.response_code


@api.app_errorhandler(EntityNotFoundException)
def handle_not_found(e: EntityNotFoundException):
    return jsonify({'message': e.message}), 404
