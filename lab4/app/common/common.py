import os
import datetime

from flask import request, render_template
menu = {
    'Home': 'home',
    'About': 'about',
    'Contacts': 'contacts',
    'Skills': 'skills'
}


def render(template: str | list[str], **kwargs):
    info = [os.name, datetime.datetime.now(), request.user_agent]
    if type(template) is list:
        template = [view + ".html" for view in template]
    else:
        template += ".html"

    return render_template(template, data=info, menu=menu, **kwargs)
