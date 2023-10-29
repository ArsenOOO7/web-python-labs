from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


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
