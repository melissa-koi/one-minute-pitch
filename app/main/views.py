from flask import render_template, redirect, url_for, flash, request
from . import main
from flask_login import login_required, current_user
from .forms import FlaskForm, CommentForm, PostForm
from ..models import Post, User, Comment

@main.route('/')
def index():
    title = 'Home - Welcome to The Pitches Website'

    return render_template('index.html', title=title)

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        post_obj = Post(post=post, title=title, category=category, user_id=user_id)
        post_obj.save()
        return redirect(url_for('main.index'))
    return render_template('pitches.html', form=form)

