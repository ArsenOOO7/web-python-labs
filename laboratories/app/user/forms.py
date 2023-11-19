from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, EmailField, DateField, FileField
from wtforms.validators import DataRequired, ValidationError, Regexp

from app.domain.User import User


class ChangePassword(FlaskForm):
    old_password = PasswordField('Old password',
                                 render_kw={'placeholder': 'Old password...'})
    new_password = PasswordField("New Password",
                                 render_kw={"placeholder": "New password..."},
                                 validators=[
                                     DataRequired(message="Password cannot be empty."),
                                     Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$', 0,
                                            'Passwords must contain minimum eight characters, at least one uppercase '
                                            'letter, one lowercase letter and one number!')
                                 ])
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary mt-md-3"})


class UpdateUserForm(FlaskForm):
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
    birth_date = DateField('Birth date',
                           render_kw={'placeholder': 'Birth date...'})
    user_image = FileField('Avatar',
                           render_kw={'placeholder': 'Avatar...', 'accept': '.jpg, .jpeg, .png'})
    about_me = TextAreaField('About me',
                             render_kw={'placeholder': 'About me...'})

    def validate_username(self, field):
        if current_user.username != field.data and User.query.filter(User.username == field.data).first():
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        if current_user.email != field.data and User.query.filter(User.email == field.data).first():
            raise ValidationError('Email already exists.')