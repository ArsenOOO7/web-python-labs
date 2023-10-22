from app import app
from app.common.common import render

my_skills = ['Java', 'PHP', 'C++', 'Spring Boot', 'Laravel', 'PostgreSQL', 'MySQL',
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
@app.route("/skills/<id>")
def skills(id=None):
    skill_name = None
    if id:
        try:
            skill_name = id if my_skills[my_skills.index(id)] == id else 'Undefined'
        except ValueError:
            skill_name = 'Undefined!'
    return render("skills",
                  skills=my_skills, skill_name=skill_name, total_len=len(my_skills))
