from functools import wraps

import jwt
from datetime import datetime, UTC, timedelta

from flask import request, jsonify

from .access_token_exception import AccessTokenException


class JwtUtils:
    ALGORITHM = 'HS256'

    def __init__(self, secret_key: str = None):
        self.__secret_key = secret_key

    def init_app(self, secret_key):
        self.__secret_key = secret_key

    def generate_token(self, subject: str, expires: int):
        payload = {
            'exp': datetime.now(UTC) + timedelta(hours=expires),
            'iat': datetime.now(UTC),
            'sub': subject
        }
        return jwt.encode(payload, self.__secret_key, self.ALGORITHM)

    def verify_jwt(self, jwt_token: str):
        if not jwt_token:
            raise AccessTokenException('Access token is required!')

        if not jwt_token.startswith(self.__secret_key):
            raise AccessTokenException('Access token is invalid!')

        try:
            token = jwt_token.split(' ')[1]
            payload = jwt.decode(token, self.__secret_key, algorithms=[self.ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise AccessTokenException('Access token is expired!')
        except jwt.InvalidTokenError:
            raise AccessTokenException('Access token is invalid!')

    def verify_permissions(self, login: str = None):
        """ Maybe for future, if it will be required by next lab(s) """
        pass

    def pre_authorize(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authentication')
            try:
                token_subject = self.verify_jwt(token)
                self.verify_permissions(token_subject)
            except AccessTokenException as e:
                return jsonify({'message': e.message}), e.response_code

            return f(args, kwargs)

        return decorated
