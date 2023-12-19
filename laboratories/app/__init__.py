from flask import Flask, url_for
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from app.swagger import swagger_bp
from app.util.jwt_utils import JwtUtils
from config import Config

data_base = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
jwt_utils = JwtUtils()
ma = Marshmallow()


def create_app(profile_name: str = None):
    app = Flask(__name__)
    profile = Config.get_profile(profile_name)
    app.config.from_object(profile)
    app.secret_key = profile.get_secret_key()

    data_base.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    jwt_utils.init_app(profile.get_secret_key(), profile.JWT_TOKEN_SECRET)

    with app.app_context():
        from .general import general_bp
        from .auth import auth_bp
        from .user import user_bp
        from .cookie import cookie_bp
        from .feedback import feedback_bp
        from .task import task_bp
        from .post import post_bp
        from app.api import api

        app.register_blueprint(general_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(cookie_bp)
        app.register_blueprint(feedback_bp)
        app.register_blueprint(task_bp)
        app.register_blueprint(post_bp, url_prefix='/post')
        app.register_blueprint(api, url_prefix='/api')
        app.register_blueprint(swagger_bp)

    return app


app = create_app()
Migrate(app, data_base)
