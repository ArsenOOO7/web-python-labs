from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, RadioField, \
    EmailField, DateField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp

from app.common import to_readable
from app.domain.Feedback import Satisfaction
from app.domain.Task import Status
from app.domain.User import User


class RegisterForm(FlaskForm):
    username = StringField("Username",
                           render_kw={'placeholder': 'Username...'},
                           validators=[
                               DataRequired(message="Username is required."),
                               Regexp("^[A-Za-z0-9\\._\\-]*$", 0,
                                      'Username should have letters, numbers, underscores, dots')
                           ])
    first_name = StringField("First name",
                             render_kw={'placeholder': 'First name...'},
                             validators=[
                                 DataRequired(message="First name is required."),
                                 Regexp('^[A-Z]{1}[a-z]*$', 0,
                                        'First name should have contain only letters with the first one capitalized')
                             ])
    last_name = StringField("Last name",
                            render_kw={'placeholder': 'Last name...'},
                            validators=[
                                DataRequired(message="Last name is required."),
                                Regexp('^[A-Z]{1}[a-z]*$', 0,
                                       'Last name should have contain only letters with the first one capitalized')
                            ])
    email = EmailField('Email',
                       render_kw={'placeholder': 'Email...'},
                       validators=[
                           DataRequired(message="Email is required.")
                       ])
    password = PasswordField('Password',
                             render_kw={'placeholder': 'Password...'},
                             validators=[
                                 DataRequired(message="Last name is required."),
                                 Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$', 0,
                                        'Passwords must contain minimum eight characters, at least one uppercase '
                                        'letter, one lowercase letter and one number!')
                             ])
    confirm_password = PasswordField('Confirm password',
                                     render_kw={'placeholder': 'Confirm password...'},
                                     validators=[
                                         DataRequired(message="Confirm password is required."),
                                         EqualTo('password')
                                     ])
    birth_date = DateField('Birth date',
                           render_kw={'placeholder': 'Birth date...'})
    user_image = FileField('Avatar',
                           render_kw={'placeholder': 'Avatar...', 'accept': '.jpg, .jpeg, .png'})

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    login = StringField("Login",
                        render_kw={"placeholder": "Login..."},
                        validators=[
                            DataRequired(message="Login cannot be empty.")
                        ])
    password = PasswordField("Password",
                             render_kw={"placeholder": "Password..."},
                             validators=[
                                 DataRequired(message="Password cannot be empty.")
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
                              choices=[(satisfaction.name, to_readable(satisfaction.value)) for satisfaction in
                                       Satisfaction],
                              validators=[
                                  DataRequired(message="Select your level of satisfaction.")
                              ])
