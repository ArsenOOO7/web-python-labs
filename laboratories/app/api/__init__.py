from flask import Blueprint

from app.api.auth_rest import oauth_bp
from app.api.household_appliances_rest import household_appliances_bp
from app.api.task_rest import task_rest_bp
from app.api.user_rest import user_rest_bp

api = Blueprint('api', __name__)

api.register_blueprint(task_rest_bp, url_prefix='/task')
api.register_blueprint(oauth_bp, url_prefix='/auth')
api.register_blueprint(user_rest_bp, url_prefix='/user')
api.register_blueprint(household_appliances_bp, url_prefix='/householdAppliance')

from . import global_exception_handler
