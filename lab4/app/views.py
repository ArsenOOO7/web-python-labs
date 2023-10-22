import datetime
import os
from app import app

from flask import Flask, render_template, request

my_skills = ['Java', 'PHP', 'C++', 'Spring Boot', 'Laravel', 'PostgreSQL', 'MySQL',
             'Elasticsearch', 'JavaScript', 'Angular', 'Python', 'Docker']

menu = {
    'Home': 'home',
    'About': 'about',
    'Contacts': 'contacts',
    'Skills': 'skills'
}


@app.route("/")
@app.route("/home")
def home():
    return render("home")


@app.route("/about")
def about():
    return render("about")


@app.route("/contacts")
def contacts():
    return render("contacts")


@app.route("/skills")
@app.route("/skills/<id>")
def skills(id=None):
    info = [os.name, datetime.datetime.now(), request.user_agent]
    skill_name = None
    if id:
        try:
            skill_name = id if my_skills[my_skills.index(id)] == id else 'Undefined'
        except ValueError:
            skill_name = 'Undefined!'
    return render_template("skills.html",
                           skills=my_skills, skill_name=skill_name, data=info, total_len=len(my_skills), menu=menu)


def render(template):
    info = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template(template + ".html", data=info, menu=menu)
