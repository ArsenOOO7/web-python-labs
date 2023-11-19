from datetime import datetime

from flask import session, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from app import data_base
from app.common.common import render, upload_file
from app.domain.User import User
from . import auth_bp
from .forms import LoginForm, RegisterForm


@auth_bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    login_form = LoginForm()
    if 'login_form_login_errors' in session:
        login_form.login.errors = session.pop('login_form_login_errors')
    if 'login_form_password_errors' in session:
        login_form.password.errors = session.pop('login_form_password_errors')
    if 'login_form_login_value' in session:
        login_form.login.data = session.pop('login_form_login_value')
    return render('login', login_form=login_form)


@auth_bp.route('/login', methods=['POST'])
def login_handle():
    login_form = LoginForm()
    session['login_form_login_value'] = login_form.login.data
    if login_form.validate_on_submit():
        login_value = login_form.login.data
        password = login_form.password.data

        user = User.query.filter(User.username == login_value).first()
        if not user or not user.verify_password(password):
            flash("Invalid credentials.", category="danger")
            return redirect(url_for('auth.login'))

        if login_form.remember.data:
            login_user(user, remember=True)
            session.pop('login_form_login_value')
            flash("You successfully logged in.", category="success")
            return redirect(url_for("cookie.info"))

    session['login_form_login_errors'] = login_form.login.errors
    session['login_form_password_errors'] = login_form.password.errors
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    register_form = RegisterForm()
    return render('register', form=register_form)


@auth_bp.route('/register', methods=['POST'])
def register_handle():
    register_form = RegisterForm()
    if not register_form.validate_on_submit():
        return render('register', form=register_form)

    username = register_form.username.data
    first_name = register_form.first_name.data
    last_name = register_form.last_name.data
    email = register_form.email.data
    password = register_form.password.data
    birth_date = register_form.birth_date.data
    avatar_file = register_form.user_image.data
    avatar_path = upload_file(avatar_file)

    user = User(username=username, first_name=first_name, last_name=last_name, email=email, birth_date=birth_date)
    user.user_password = password
    if avatar_path:
        user.avatar_file = avatar_path

    data_base.session.add(user)
    data_base.session.commit()
    flash(f"You successfully created an account {register_form.username.data}!", category='success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out!', category="success")
    return redirect(url_for('auth.login'))


@auth_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            data_base.session.commit()
        except:
            flash(f"Error on updating last seen", category='danger')
    return response
