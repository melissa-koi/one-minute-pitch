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
        user_id = current_user
        post = form.post.data
        category = form.category.data
        post_obj = Post(title=title, user_id=user_id, post=post, category=category)
        post_obj.save_post()
        return redirect(url_for('main.posts'))
    return render_template('pitches.html', form=form)

@main.route('/posts')
@login_required
def posts():
    interview = Post.query.filter_by(category = 'Interview Pitch').all()
    sales = Post.query.filter_by(category = 'Sales Pitch').all()
    promotion = Post.query.filter_by(category = 'Promotion Pitch').all()
    pickup_lines = Post.query.filter_by(category = 'Pickup Lines').all()
    business = Post.query.filter_by(category = 'Business Pitch').all()

    return render_template('posts.html', interview = interview, sales = sales, promotion = promotion, pickup_lines = pickup_lines, business = business)

