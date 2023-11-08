from app import app
from app.common.common import render
from .forms import LoginForm, ChangePassword, RegisterForm
from flask import request, session, redirect, make_response, url_for, flash
import json


@app.route('/login', methods=['GET'])
def login():
    login_form = LoginForm()
    if 'login_form_login_errors' in session:
        login_form.login.errors = session.pop('login_form_login_errors')
    if 'login_form_password_errors' in session:
        login_form.password.errors = session.pop('login_form_password_errors')
    if 'login_form_login_value' in session:
        login_form.login.data = session.pop('login_form_login_value')
    return render('user/login', login_form=login_form)


@app.route('/login', methods=['POST'])
def login_handle():
    login_form = LoginForm()
    session['login_form_login_value'] = login_form.login.data
    if login_form.validate_on_submit():
        with open('resources/users.json', 'r') as users:
            login_value = login_form.login.data
            password = login_form.password.data
            json_data = json.load(users)
            if json_data.get(login_value) is not None:
                user_data = json_data[login_value]
                if user_data['password'] == password:
                    del user_data['password']
                    if login_form.remember.data:
                        session['user'] = user_data
                        session['user']['login'] = login_value
                        session.pop('login_form_login_value')
                    flash("You successfully logged in.", category="success")
                    return redirect(url_for("info"))
            flash("Invalid credentials.", category="danger")
            return redirect(url_for('login'))
    session['login_form_login_errors'] = login_form.login.errors
    session['login_form_password_errors'] = login_form.password.errors
    return redirect(url_for('login'))


@app.route('/register', methods=['GET'])
def register():
    register_form = RegisterForm()
    return render('user/register', form=register_form)


@app.route('/register_handle', methods=['POST'])
def register_handle():
    register_form = RegisterForm()
    if not register_form.validate_on_submit():
        return render('user/register', form=register_form)

    flash(f"You successfully created an account {register_form.username.data}!", category='success')
    return redirect(url_for('login'))


@app.route('/info')
def info():
    if session.get('user') is None:
        return redirect(url_for('login'))
    cookies = request.cookies.items()
    change_password_form = ChangePassword()
    if 'form_cp_errors' in session:
        change_password_form.new_password.errors = session.pop('form_cp_errors')
    return render('user/info', cookies=cookies, change_password_form=change_password_form)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out!', category="success")
    return redirect(url_for('login'))


@app.route("/cookie", methods=['POST'])
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
def clear_cookie(cookie_name=None):
    if request.method == "POST":
        response = make_response(redirect(url_for('info')))
        for cookie in request.cookies.keys():
            if cookie != 'session':
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


@app.route('/change_password', methods=['POST'])
def change_password():
    change_password_form = ChangePassword()
    if change_password_form.validate_on_submit():
        new_password = change_password_form.new_password.data
        user_login = session['user']['login']
        with open('resources/users.json', 'r') as file:
            data = json.load(file)
        data[user_login]['password'] = new_password

        with open('resources/users.json', 'w') as file:
            json.dump(data, file)
        flash("You successfully changed your password!", category="success")
        return redirect(url_for('info'))
    session['form_cp_errors'] = change_password_form.new_password.errors
    return redirect(url_for('info'))
