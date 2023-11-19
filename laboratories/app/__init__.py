from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import APP_SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
data_base = SQLAlchemy(app)

migrate = Migrate(app, data_base)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from .general import general_bp
from .auth import auth_bp
from .user import user_bp
from .cookie import cookie_bp
from .feedback import feedback_bp

app.register_blueprint(general_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(cookie_bp)
app.register_blueprint(feedback_bp)

from app import task_controller
