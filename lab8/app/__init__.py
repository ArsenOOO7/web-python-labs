from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = b"secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laboratory_work.db'
data_base = SQLAlchemy(app)

migrate = Migrate(app, data_base)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import main_controller
from app import task_controller
from app import user_controller
from app import feedback_controller
