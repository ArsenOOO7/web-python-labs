from app import app
from app.common.common import render
from flask import request, session, redirect


@app.route('/login', methods=['GET'])
def login():
    return render('user/login')


@app.route('/login', methods=['POST'])
def loginHandle():
    pass


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
