from app import app
from app.common.common import render
from flask import request, session, redirect
import json


@app.route('/login', methods=['GET'])
def login():
    return render('user/login')


@app.route('/login', methods=['POST'])
def login_handle():
    login = request.form.get('login')
    password = request.form.get('password')
    with open('resources/users.json', 'r') as users:
        json_data = json.load(users)
        if json_data.get(login) is not None:
            user_data = json_data[login]
            if user_data['password'] == password:
                session['user'] = user_data
                session['user']['login'] = login
                return redirect('/info')
        session['login_error'] = 'Invalid credentials'
        return redirect('/login')


@app.route('/info')
def info():
    if session.get('user') is None:
        return redirect('/login')
    return render('user/info')


@app.route('/logout')
def logout():
    if session.get('user') is None:
        return redirect('/login')
    session.clear()
    return redirect('/')
