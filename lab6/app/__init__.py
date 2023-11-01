from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b"secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laboratory_work.db'
data_base = SQLAlchemy(app)

from app.domain import Task

with app.app_context():
    data_base.create_all()

from app import main_controller
from app import task_controller
from app import user_controller
