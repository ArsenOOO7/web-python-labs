from flask import Flask, render_template, request
import os, datetime

app = Flask(__name__)

my_skills = ['Java', 'PHP', 'C++' 'Spring Boot', 'Laravel', 'PostgreSQL', 'MySQL',
             'Elasticsearch', 'JavaScript', 'Angular', 'Python', 'Docker']

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
@app.route("/skills/<int:id>")
def skills(id=None):
    return render("skills")

def render(template):
    info = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template(template + ".html", data=info)


if __name__ == '__main__':
    app.run()
