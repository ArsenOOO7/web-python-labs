from app.common.common import render
from . import general_bp

my_skills = ['Java', 'PHP', 'C++', 'Spring Boot', 'Laravel', 'PostgreSQL', 'MySQL',
             'Elasticsearch', 'JavaScript', 'Angular', 'Python', 'Docker']


@general_bp.route("/")
@general_bp.route("/home")
def home():
    return render("home")


@general_bp.route("/about")
def about():
    return render("about")


@general_bp.route("/contacts")
def contacts():
    return render("contacts")


@general_bp.route("/skills")
@general_bp.route("/skills/<id>")
def skills(id=None):
    skill_name = None
    if id:
        try:
            skill_name = id if my_skills[my_skills.index(id)] == id else 'Undefined'
        except ValueError:
            skill_name = 'Undefined!'
    return render("skills",
                  skills=my_skills, skill_name=skill_name, total_len=len(my_skills))
