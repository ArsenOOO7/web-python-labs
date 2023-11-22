from flask import Blueprint
from .category import category_bp

post_bp = Blueprint("post", __name__, template_folder="templates", static_folder="static")
post_bp.register_blueprint(category_bp, url_prefix='category')

from . import controller
