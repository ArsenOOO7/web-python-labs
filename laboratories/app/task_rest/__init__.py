from flask import Blueprint

task_rest_bp = Blueprint("task_rest", __name__)

from . import controller
