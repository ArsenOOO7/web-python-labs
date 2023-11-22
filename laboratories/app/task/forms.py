from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from app.domain.Task import Status


class AddTask(FlaskForm):
    name = StringField("Name",
                       render_kw={"placeholder": "Name..."},
                       validators=[
                           DataRequired(message="Task name is required.")
                       ])
    description = TextAreaField("Description", render_kw={"placeholder": "Description..."})


class UpdateTask(FlaskForm):
    name = StringField("Name",
                       render_kw={"placeholder": "Name..."},
                       validators=[
                           DataRequired(message="Task name is required.")
                       ])
    description = TextAreaField("Description", render_kw={"placeholder": "Description..."})
    status = SelectField("Status", choices=Status.get_dropdown_values())
