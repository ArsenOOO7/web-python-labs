from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from app import data_base
from app.common.common import render, to_readable
from app.domain.Post import Post, PostType
from . import post_bp


@post_bp.route("/", methods=['POST'])
def create_post():
    pass


@post_bp.route("/<int:id>", methods=['POST'])
def update_post():
    pass


@post_bp.route('/<int:id>')
def get_post(id=None):
    pass


@post_bp.route('/<int:id>/delete')
def delete_post():
    pass
