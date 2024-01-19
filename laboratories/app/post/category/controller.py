from flask import redirect, url_for, flash
from flask_login import login_required

from app import data_base
from app.common.common import render
from app.domain.Category import Category
from . import category_bp
from .forms import CategoryForm


@category_bp.route("/create", methods=['GET'])
@login_required
def create_category():
    form = CategoryForm()
    return render('create_category', form=form)


@category_bp.route("/create", methods=['POST'])
@login_required
def create_category_handle():
    form = CategoryForm()
    if not form.validate_on_submit():
        return render('create_category', form=form)

    name = form.name.data
    category = Category(name=name)

    data_base.session.add(category)
    data_base.session.commit()

    flash(f"You have successfully created category {name}.", category='success')
    return redirect(url_for('post.category.category_list'))


@category_bp.route("/<int:id>/update", methods=['GET'])
@login_required
def update_category(id=None):
    if id is None:
        return redirect(url_for('post.category.category_list'))

    category = Category.query.get_or_404(id)
    form = CategoryForm(category.id)
    form.name.data = category.name

    return render('update_category', form=form, category=category)


@category_bp.route("/<int:id>/update", methods=['POST'])
@login_required
def update_category_handle(id=None):
    if id is None:
        return redirect(url_for('post.category.category_list'))

    category = Category.query.get_or_404(id)
    form = CategoryForm(id)
    if not form.validate_on_submit():
        return render('update_category', form=form, category=category)

    name = form.name.data
    category.name = name

    data_base.session.commit()
    flash("You successfully updated your Category!", category="success")
    return redirect(url_for('post.category.category_list'))


@category_bp.route('/list', methods=['GET'])
@login_required
def category_list():
    categories = Category.query.all()
    return render('categories', categories=categories)


@category_bp.route('/<int:id>/delete')
@login_required
def delete_category(id=None):
    if id is None:
        return redirect(url_for('post.category.category_list'))

    category = Category.query.get_or_404(id)
    data_base.session.delete(category)
    data_base.session.commit()
    flash('You successfully deleted ur category.', category='success')

    return redirect(url_for('post.category.category_list'))
