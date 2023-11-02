from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length

from app.domain.Feedback import Satisfaction
from app.domain.Task import Status
from app.common import to_readable


class LoginForm(FlaskForm):
    login = StringField("Login",
                        render_kw={"placeholder": "Login..."},
                        validators=[
                            DataRequired(message="Login cannot be empty.")
                        ])
    password = PasswordField("Password",
                             render_kw={"placeholder": "Password..."},
                             validators=[
                                 DataRequired(message="Password cannot be empty."),
                                 Length(min=4, max=10)
                             ])
    remember = BooleanField("Remember", default=False)


class ChangePassword(FlaskForm):
    new_password = PasswordField("New Password",
                                 render_kw={"placeholder": "New password..."},
                                 validators=[
                                     DataRequired(message="Password cannot be empty."),
                                     Length(min=4, max=10)
                                 ])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-md-3"})


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

class AddFeedback(FlaskForm):
    feedback = TextAreaField("Feedback",
                             render_kw={'placeholder': 'Give your feedback...'},
                             validators=[
                                 DataRequired(message="Feedback is required.")
                             ])
    satisfaction = RadioField("Satisfaction",
                              choices=[(satisfaction.name, to_readable(satisfaction.value)) for satisfaction in Satisfaction],
                              validators=[
                                  DataRequired(message="Select your level of satisfaction.")
                              ])