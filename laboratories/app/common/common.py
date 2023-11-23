import datetime
import os
import uuid

from PIL import Image
from flask import request, render_template

from config import IMAGES_DEFAULT_NAME, IMAGES_FOLDER

menu = {
    'Home': 'general.home',
    'About': 'general.about',
    'Contacts': 'general.contacts',
    'Skills': 'general.skills',
    'Tasks': 'task.tasks',
    'Feedback': 'feedback.feedback'
}

authorized_menu = {
    'Users': ['user.users', True],
    'Login': ['auth.login', False],
    'Register': ['auth.register', False],
    'Cookies': ['cookie.info', True],
    'Account': ['user.account', True],
    'Posts': ['post.get_post', True],
    'Categories': ['post.category.category_list', True],
    'Tags': ['post.tag.tag_list', True],
    'Logout': ['auth.logout', True]
}


def render(template: str | list[str], **kwargs):
    info = [os.name, datetime.datetime.now(), request.user_agent]
    if type(template) is list:
        template = [view + ".html" for view in template]
    else:
        template += ".html"

    return render_template(template, data=info, menu=menu, authorized_menu=authorized_menu, **kwargs)


def to_readable(value: str):
    return value.replace("_", " ").lower().capitalize()


def delete_file(file_name):
    path = os.path.join(IMAGES_FOLDER, file_name)
    if file_name != IMAGES_DEFAULT_NAME and os.path.exists(path):
        os.remove(path)


def upload_file(file):
    if not file:
        return False
    filename, extension = file.filename.rsplit('.', 1)
    uuid_name = uuid.uuid4()
    secured_filename = f"{uuid_name}.{extension}"
    path = os.path.join(IMAGES_FOLDER, secured_filename)

    image = Image.open(file)
    image.thumbnail((512, 512))
    image.save(path)
    return secured_filename
