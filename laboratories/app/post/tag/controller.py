from flask import redirect, url_for, flash
from flask_login import login_required

from app import data_base
from app.common.common import render, to_readable
from . import tag_bp
from .forms import TagForm
from app.domain.Tag import Tag, Color


@tag_bp.route("/create", methods=['GET'])
@login_required
def create_tag():
    form = TagForm()
    return render('create_tag', form=form)


@tag_bp.route("/create", methods=['POST'])
@login_required
def create_tag_handle():
    form = TagForm()
    if not form.validate_on_submit():
        return render('create_tag', form=form)

    name = form.name.data
    color = Color[form.color.data]
    tag = Tag(name=name, color=color)

    data_base.session.add(tag)
    data_base.session.commit()

    flash(f"You have successfully created Tag {name}.", category='success')
    return redirect(url_for('post.tag.tag_list'))


@tag_bp.route("/<int:id>/update", methods=['GET'])
@login_required
def update_tag(id=None):
    if id is None:
        return redirect(url_for('post.tag.tag_list'))

    tag = Tag.query.get_or_404(id)
    form = TagForm(tag.id)
    form.color.default = tag.color.name
    form.process()

    return render('update_tag', form=form, tag=tag)


@tag_bp.route("/<int:id>/update", methods=['POST'])
@login_required
def update_tag_handle(id=None):
    if id is None:
        return redirect(url_for('post.tag.tag_list'))

    tag = Tag.query.get_or_404(id)
    form = TagForm(id)
    if not form.validate_on_submit():
        return render('update_tag', form=form, tag=tag)

    name = form.name.data
    tag.name = name
    tag.color = Color[form.color.data]

    data_base.session.commit()
    flash("You successfully updated your Tag!", category="success")
    return redirect(url_for('post.tag.tag_list'))


@tag_bp.route('/list', methods=['GET'])
@login_required
def tag_list():
    tags = Tag.query.all()
    return render('tags', tags=tags)


@tag_bp.route('/<int:id>/delete')
@login_required
def delete_tag(id=None):
    if id is None:
        return redirect(url_for('post.tag.tag_list'))

    tags = Tag.query.get_or_404(id)
    data_base.session.delete(tags)
    data_base.session.commit()
    flash('You successfully deleted ur tag.', category='success')

    return redirect(url_for('post.tag.tag_list'))
