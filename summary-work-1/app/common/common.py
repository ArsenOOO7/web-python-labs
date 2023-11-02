import os
import datetime

from flask import request, render_template, session, redirect, url_for

menu = {
    'Home': 'home',
    'About': 'about',
    'Contacts': 'contacts',
    'Skills': 'skills',
    'Tasks': 'tasks'
}

authorized_menu = {
    'Login': ['login', False],
    'Information': ['info', True],
    'Logout': ['logout', True]
}


def render(template: str | list[str], **kwargs):
    info = [os.name, datetime.datetime.now(), request.user_agent]
    if type(template) is list:
        template = [view + ".html" for view in template]
    else:
        template += ".html"

    return render_template(template, data=info, menu=menu, authorized_menu=authorized_menu, **kwargs)
