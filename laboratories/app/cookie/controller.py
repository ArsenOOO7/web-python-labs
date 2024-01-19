from flask import request, session, redirect, make_response, url_for, flash
from flask_login import login_required

from app.common.common import render
from . import cookie_bp


@cookie_bp.route('/info')
@login_required
def info():
    cookies = request.cookies.items()
    return render('info', cookies=cookies)


@cookie_bp.route("/cookie", methods=['POST'])
@login_required
def add_cookie():
    cookie_name = request.form.get('cookie_name')
    cookie_value = request.form.get('cookie_value')
    cookie_expires_at = request.form.get('expires_at')
    response = make_response(redirect(url_for('cookie.info')))
    response.set_cookie(cookie_name, cookie_value, expires=cookie_expires_at)
    flash(f"You have successfully created a cookie {cookie_name}", category="success")
    return response


@cookie_bp.route('/clear_cookie', methods=['POST'])
@cookie_bp.route('/clear_cookie/<cookie_name>', methods=['GET'])
@login_required
def clear_cookie(cookie_name=None):
    if request.method == "POST":
        response = make_response(redirect(url_for('cookie.info')))
        for cookie in request.cookies.keys():
            if cookie != 'session' and cookie != 'remember_token':
                response.delete_cookie(cookie)
        flash("You have successfully deleted all cookies", category="success")
        return response

    if cookie_name is None:
        return redirect(url_for('cookie.info'))

    if cookie_name not in request.cookies.keys():
        session['cookie_error'] = f"Undefined cookie {cookie_name}"
        flash(f"Undefined cookie {cookie_name}", category="danger")
        return redirect(url_for('cookie.info'))

    flash(f"You have successfully deleted cookie {cookie_name}", category="success")
    response = make_response(redirect(url_for('cookie.info')))
    response.delete_cookie(cookie_name)
    return response
