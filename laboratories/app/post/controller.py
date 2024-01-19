from flask import redirect, url_for, flash, request
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import data_base
from app.common.common import render, upload_file, delete_file, to_readable
from app.domain.Post import Post, PostType
from constant import POST_PAGINATION_SIZE
from . import post_bp
from .forms import PostForm, CategorySearchForm
from ..domain.Category import Category
from ..domain.Tag import Tag


def populate_form(form: PostForm):
    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]
    form.tags.choices = [(tag.name, tag.name) for tag in Tag.query.all()]


@post_bp.route("/create", methods=['GET'])
@login_required
def create_post():
    form = PostForm()
    populate_form(form)
    return render('create_post', form=form)


@post_bp.route("/create", methods=['POST'])
@login_required
def create_post_handle():
    form = PostForm()
    populate_form(form)
    if not form.validate_on_submit():
        return render('create_post', form=form)

    title = form.title.data
    text = form.text.data
    enabled = form.enabled.data
    post_type = form.type.data
    category_id = form.categories.data
    tags = [tag for tag in Tag.query.filter(Tag.name.in_(form.tags.data)).all()]

    post = Post(title=title, text=text, enabled=enabled, type=post_type, user_id=current_user.id,
                category_id=category_id, tags=tags)

    image = upload_file(form.image.data)
    if image:
        post.image = image

    data_base.session.add(post)
    data_base.session.commit()

    flash("You successfully created post!", category='success')
    return redirect(url_for('post.post_list'))


@post_bp.route("/<int:id>/update", methods=['GET'])
@login_required
def update_post(id=None):
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    form = PostForm()
    populate_form(form)
    form.text.default = post.text
    form.type.default = post.type.name
    form.categories.default = post.category_id
    form.tags.default = [tag.name for tag in post.tags]
    form.process()

    return render('update_post', form=form, post=post)


@post_bp.route("/<int:id>/update", methods=['POST'])
@login_required
def update_post_handle(id=None):
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    form = PostForm()
    populate_form(form)
    if not form.validate_on_submit():
        return render('post', form=form, post=post)

    post.title = form.title.data
    post.text = form.text.data
    post.type = PostType[form.type.data]
    post.enabled = form.enabled.data
    post.category_id = form.categories.data
    post.tags = [tag for tag in Tag.query.filter(Tag.name.in_(form.tags.data)).all()]

    if form.image.data:
        delete_file(post.image)
        post.image = upload_file(form.image.data)

    data_base.session.commit()
    flash("You successfully updated your post!", category="success")
    return redirect(url_for('post.post_list'))


@post_bp.route('/list', methods=['GET'])
@login_required
def post_list():
    form = CategorySearchForm(request.args, meta={'csrf': False})
    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]
    page = request.args.get('page', 1, type=int)

    query = Post.query
    if form.validate():
        category_id = form.categories.data
        query = query.filter(Post.category_id == category_id)
    else:
        form.categories.errors = []

    posts = query.order_by(desc(Post.created_at)).paginate(page=page, per_page=POST_PAGINATION_SIZE)
    return render('posts', posts=posts, form=form)


@post_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_post(id=None):
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    return render('post', post=post, to_readable=to_readable)


@post_bp.route('/<int:id>/delete')
@login_required
def delete_post(id=None):
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    if post.user_id == current_user.id:
        data_base.session.delete(post)
        data_base.session.commit()
        flash('You successfully deleted ur post.', category='success')
    else:
        flash("You cannot delete this post!", category='danger')

    return redirect(url_for('post.post_list'))
