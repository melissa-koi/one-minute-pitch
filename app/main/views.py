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
        user_id = current_user._get_current_object().id
        category = form.category.data
        author = form.author.data
        post_obj = Post(title=title, post=post,user_id = user_id, category=category, author = author)
        post_obj.save_post()
        return redirect(url_for('main.posts'))
    return render_template('pitches.html', form=form)

@main.route('/posts')
@login_required
def posts():
    posts_display = Post.query.all()

    return render_template('posts.html', posts_display = posts_display)

