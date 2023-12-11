from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

data_base = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(profile_name: str = None):
    app = Flask(__name__)
    profile = Config.get_profile(profile_name)
    app.config.from_object(profile)
    app.secret_key = profile.get_secret_key()

    data_base.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .general import general_bp
        from .auth import auth_bp
        from .user import user_bp
        from .cookie import cookie_bp
        from .feedback import feedback_bp
        from .task import task_bp
        from .post import post_bp
        from .task_rest import task_rest_bp

        app.register_blueprint(general_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(cookie_bp)
        app.register_blueprint(feedback_bp)
        app.register_blueprint(task_bp)
        app.register_blueprint(post_bp, url_prefix='/post')
        app.register_blueprint(task_rest_bp, url_prefix='/api/task')

    return app


app = create_app()
Migrate(app, data_base)