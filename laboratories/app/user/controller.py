from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from app import data_base
from app.domain.User import User
from app.common.common import render, upload_file, delete_file
from . import user_bp
from .forms import UpdateUserForm
from app.auth.forms import ChangePassword


@user_bp.route('/account', methods=['GET'])
@login_required
def account():
    form = UpdateUserForm()
    form.about_me.data = current_user.about_me
    change_password_form = ChangePassword()
    return render('account', form=form, change_password_form=change_password_form)


@user_bp.route('/account', methods=['POST'])
@login_required
def update_account():
    form = UpdateUserForm()
    if not form.validate_on_submit():
        return render('account', form=form)

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
    return redirect(url_for('user.account'))


@user_bp.route('/users')
def users():
    all_users = [user.create_user_details() for user in User.query.all()]
    return render('users', users=all_users)
