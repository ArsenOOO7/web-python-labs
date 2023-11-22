from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from app import data_base
from app.common.common import render, to_readable, upload_file, delete_file
from app.domain.Post import Post, PostType
from . import post_bp
from .forms import PostForm


@post_bp.route("/", methods=['GET'])
@login_required
def create_post():
    form = PostForm()
    return render('create_post', form=form)


@post_bp.route("/", methods=['POST'])
@login_required
def create_post_handle():
    form = PostForm()
    if not form.validate_on_submit():
        return render('create_post', form=form)

    title = form.title.data
    text = form.text.data
    enabled = form.enabled.data
    post_type = form.type.data

    post = Post(title=title, text=text, enabled=enabled, type=post_type, user_id=current_user.id)

    image = upload_file(form.image.data)
    if image:
        post.image = image

    data_base.session.add(post)
    data_base.session.commit()

    flash("You successfylly created post!", category='success')
    return redirect(url_for('post.get_post'))


@post_bp.route("/<int:id>", methods=['POST'])
@login_required
def update_post(id=None):
    if id is None:
        return redirect(url_for('post.get_post'))

    post = Post.query.get_or_404(id)
    form = PostForm()
    if not form.validate_on_submit():
        return render('post', form=form, post=post)

    post.title = form.title.data
    post.text = form.text.data
    post.type = form.type.data
    post.enabled = form.enabled.data

    if form.image.data:
        delete_file(post.image)
        post.image = upload_file(form.image.data)

    data_base.session.commit()
    flash("You successfully updated your post!", category="success")
    return redirect(url_for('task.get_post'))


@post_bp.route('/', methods=['GET'])
@post_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_post(id=None):
    if id is None:
        posts = Post.query.all()
        return render('posts', posts=posts)

    post = Post.query.get_or_404(id)
    form = PostForm()
    return render('post', form=form, post=post)


@post_bp.route('/<int:id>/delete')
@login_required
def delete_post(id=None):
    if id is None:
        return redirect(url_for('post.get_post'))

    post = Post.query.get_or_404(id)
    if post.user_id == current_user.id:
        Post.query.delete(id)
        flash('You successfully deleted ur post.', category='success')
    else:
        flash("You cannot delete this post!", category='danger')

    return redirect(url_for('post.get_post'))
