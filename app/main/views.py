from flask import render_template, redirect, url_for, flash, request, abort
from . import main
from flask_login import login_required, current_user
from .forms import FlaskForm, CommentForm, PostForm
from ..models import Post, User, Comment, Upvote, Downvote

@main.route('/')
def index():
    title = 'Home - Welcome to The Pitches Website'
    return render_template('index.html', title=title)

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = form.post.data
        user_id = current_user._get_current_object().id
        category = form.category.data
        author = form.author.data
        post_obj = Post(post=post,user_id = user_id, category=category, author = author)
        post_obj.save_post()
        return redirect(url_for('main.posts'))
    return render_template('pitches.html', form=form)

@main.route('/posts')
@login_required
def posts():
    posts_display = Post.query.all()
    likes = Upvote.query.all()
    user = current_user
    return render_template('posts.html', posts_display = posts_display, posts=posts, likes=likes, user=user)

@main.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    user = User.query.all()
    comments = Comment.query.filter_by(post_id=post_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment,
            post_id=post_id,
            user_id=user_id
        )
        new_comment.save()
        # new_comments = [new_comment]
        print(new_comments)
        return redirect(url_for('.comment', post_id=post_id))
    return render_template('comments.html', form=form, post=post, comments=comments, user=user)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    uname = current_user.username
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template('profile/profile.html', user=user)


@main.route('/user/<name>/update_profile', methods=['POST', 'GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username=name).first()
    if user is None:
        error = 'The user does not exist'
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile', name=name))
    return render_template('profile/update_profile.html', form=form)


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    post = Post.query.get(id)
    vote_mpya = Upvote(post=post, upvote=1)
    vote_mpya.save()
    return redirect(url_for('main.posts'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    post = Post.query.get(id)
    vm = Downvote(post=post, downvote=1)
    vm.save()
    return redirect(url_for('main.posts'))
