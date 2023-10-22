from app import app
from app.common.common import render
from flask import request, session, redirect, make_response, url_for
import json


@app.route('/login', methods=['GET'])
def login():
    return render('user/login')


@app.route('/login', methods=['POST'])
def login_handle():
    login_value = request.form.get('login')
    password = request.form.get('password')
    with open('resources/users.json', 'r') as users:
        json_data = json.load(users)
        if json_data.get(login_value) is not None:
            user_data = json_data[login_value]
            if user_data['password'] == password:
                del user_data['password']
                session['user'] = user_data
                session['user']['login'] = login_value
                return redirect('/info')
        session['login_error'] = 'Invalid credentials'
        return redirect(url_for('login'))


@app.route('/info')
def info():
    if session.get('user') is None:
        return redirect(url_for('login'))
    cookies = request.cookies.items()
    return render('user/info', cookies=cookies)


@app.route('/logout')
def logout():
    session.clear()
    session['logout'] = 'You have successfully logged out!'
    return redirect(url_for('login'))


@app.route("/cookie", methods=['POST'])
def add_cookie():
    cookie_name = request.form.get('cookie_name')
    cookie_value = request.form.get('cookie_value')
    cookie_expires_at = request.form.get('expires_at')
    session['cookie_created'] = f"You have successfully created a cookie {cookie_name}"
    response = make_response(redirect(url_for('info')))
    response.set_cookie(cookie_name, cookie_value, expires=cookie_expires_at)
    return response


@app.route('/clear_cookie', methods=['POST'])
@app.route('/clear_cookie/<cookie_name>', methods=['GET'])
def clear_cookie(cookie_name=None):
    if request.method == "POST":
        session['cookie_deleted'] = f"You have successfully deleted all cookies"
        response = make_response(redirect(url_for('info')))
        for cookie in request.cookies.keys():
            if cookie is not 'session':
                response.delete_cookie(cookie)
        return response

    if cookie_name is None:
        return redirect(url_for('info'))

    if cookie_name not in request.cookies.keys():
        session['cookie_error'] = f"Undefined cookie {cookie_name}"
        return redirect(url_for('info'))

    session['cookie_deleted'] = f"You have successfully deleted cookie {cookie_name}"
    response = make_response(redirect(url_for('info')))
    response.delete_cookie(cookie_name)
    return response


@app.route('/change_password', methods=['POST'])
def change_password():
    new_password = request.form.get('new_password')
    user_login = session['user']['login']
    with open('resources/users.json', 'r') as file:
        data = json.load(file)
    data[user_login]['password'] = new_password

    with open('resources/users.json', 'w') as file:
        json.dump(data, file)

    session['password_changed'] = "You successfully changed your password!"
    return redirect(url_for('info'))
