from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, DateField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp

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
