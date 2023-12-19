from flask import request, jsonify

from app import jwt_utils
from app.domain.User import User
from . import oauth_bp


@oauth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if data:
        login_value = data['login']
        password = data['password']
        user = User.query.filter(User.email == login_value or User.username == login_value).first()
        if user and user.verify_password(password):
            username = user.username
            access_token = jwt_utils.generate_token(username, 1)
            return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid credentials.'}), 401
