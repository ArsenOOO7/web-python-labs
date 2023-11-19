from datetime import datetime

from flask import request, session, redirect, make_response, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from app import app, data_base
from app.common.common import render, upload_file, delete_file
from .domain.User import User
from .forms import LoginForm, ChangePassword, RegisterForm, UpdateUserForm


# @app.route('/login', methods=['GET'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('info'))
#     login_form = LoginForm()
#     if 'login_form_login_errors' in session:
#         login_form.login.errors = session.pop('login_form_login_errors')
#     if 'login_form_password_errors' in session:
#         login_form.password.errors = session.pop('login_form_password_errors')
#     if 'login_form_login_value' in session:
#         login_form.login.data = session.pop('login_form_login_value')
#     return render('user/login', login_form=login_form)
#
#
# @app.route('/login', methods=['POST'])
# def login_handle():
#     login_form = LoginForm()
#     session['login_form_login_value'] = login_form.login.data
#     if login_form.validate_on_submit():
#         login_value = login_form.login.data
#         password = login_form.password.data
#
#         user = User.query.filter(User.username == login_value).first()
#         if not user or not user.verify_password(password):
#             flash("Invalid credentials.", category="danger")
#             return redirect(url_for('login'))
#
#         if login_form.remember.data:
#             login_user(user, remember=True)
#             session.pop('login_form_login_value')
#             flash("You successfully logged in.", category="success")
#             return redirect(url_for("info"))
#
#     session['login_form_login_errors'] = login_form.login.errors
#     session['login_form_password_errors'] = login_form.password.errors
#     return redirect(url_for('login'))
#
#
# @app.route('/register', methods=['GET'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('info'))
#     register_form = RegisterForm()
#     return render('user/register', form=register_form)
#
#
# @app.route('/register', methods=['POST'])
# def register_handle():
#     register_form = RegisterForm()
#     if not register_form.validate_on_submit():
#         return render('user/register', form=register_form)
#
#     username = register_form.username.data
#     first_name = register_form.first_name.data
#     last_name = register_form.last_name.data
#     email = register_form.email.data
#     password = register_form.password.data
#     birth_date = register_form.birth_date.data
#     avatar_file = register_form.user_image.data
#     upload_file(avatar_file)
#
#     user = User(username=username, first_name=first_name, last_name=last_name, email=email, birth_date=birth_date)
#     user.user_password = password
#
#     data_base.session.add(user)
#     data_base.session.commit()
#     flash(f"You successfully created an account {register_form.username.data}!", category='success')
#     return redirect(url_for('login'))


@app.route('/info')
@login_required
def info():
    cookies = request.cookies.items()
    change_password_form = ChangePassword()
    if 'form_cp_errors' in session:
        change_password_form.new_password.errors = session.pop('form_cp_errors')
    return render('user/info', cookies=cookies, change_password_form=change_password_form)


@app.route('/account', methods=['GET'])
@login_required
def account():
    form = UpdateUserForm()
    form.about_me.data = current_user.about_me
    return render('user/account', form=form)


@app.route('/account', methods=['POST'])
@login_required
def update_account():
    form = UpdateUserForm()
    if not form.validate_on_submit():
        return render('user/account', form=form)

    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.birth_date = form.birth_date.data
    current_user.about_me = form.about_me.data

    if form.user_image.data:
        delete_file(current_user.avatar_file)
        current_user.avatar_file = upload_file(form.user_image.data)

    data_base.session.commit()

    flash('You successfully updated your account details!', category='success')
    return redirect(url_for('account'))


@app.route('/users')
def users():
    all_users = [user.create_user_details() for user in User.query.all()]
    return render('user/users', users=all_users)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have successfully logged out!', category="success")
#     return redirect(url_for('login'))


@app.route("/cookie", methods=['POST'])
@login_required
def add_cookie():
    cookie_name = request.form.get('cookie_name')
    cookie_value = request.form.get('cookie_value')
    cookie_expires_at = request.form.get('expires_at')
    response = make_response(redirect(url_for('info')))
    response.set_cookie(cookie_name, cookie_value, expires=cookie_expires_at)
    flash(f"You have successfully created a cookie {cookie_name}", category="success")
    return response


@app.route('/clear_cookie', methods=['POST'])
@app.route('/clear_cookie/<cookie_name>', methods=['GET'])
@login_required
def clear_cookie(cookie_name=None):
    if request.method == "POST":
        response = make_response(redirect(url_for('info')))
        for cookie in request.cookies.keys():
            if cookie != 'session' and cookie != 'remember_token':
                response.delete_cookie(cookie)
        flash("You have successfully deleted all cookies", category="success")
        return response

    if cookie_name is None:
        return redirect(url_for('info'))

    if cookie_name not in request.cookies.keys():
        session['cookie_error'] = f"Undefined cookie {cookie_name}"
        flash(f"Undefined cookie {cookie_name}", category="danger")
        return redirect(url_for('info'))

    flash(f"You have successfully deleted cookie {cookie_name}", category="success")
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(cookie_name)
    return response


# @app.route('/change_password', methods=['POST'])
# @login_required
# def change_password():
#     change_password_form = ChangePassword()
#     if change_password_form.validate_on_submit():
#         old_password = change_password_form.old_password.data
#
#         if not current_user.verify_password(old_password):
#             flash('Incorrect old password.', category='danger')
#             return redirect(url_for('info'))
#
#         new_password = change_password_form.new_password.data
#         user_login = current_user.username
#
#         user = User.query.filter(User.username == user_login).first()
#         user.user_password = new_password
#         data_base.session.commit()
#
#         flash("You successfully changed your password!", category="success")
#         return redirect(url_for('info'))
#     session['form_cp_errors'] = change_password_form.new_password.errors
#     return redirect(url_for('info'))


@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            data_base.session.commit()
        except:
            flash(f"Error on updating last seen", category='danger')
    return response
