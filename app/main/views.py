from flask import render_template, redirect, url_for, flash, request, abort
from . import main
from flask_login import login_required, current_user
from .forms import FlaskForm, CommentForm, PostForm, UpdateProfile
from ..models import Post, User, Comment, Upvote, Downvote
from .. import db, photos

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
    return render_template('add_pitch.html', form=form)

@main.route('/posts')
@login_required
def posts():
    posts_display = Post.query.all()
    likes = Upvote.query.all()
    user = current_user
    return render_template('posts.html', posts_display = posts_display, posts=posts, likes=likes, user=user)

@main.route('/comments', methods=['GET', 'POST'])
@login_required
def comment():
    form = CommentForm()
    comments = Comment.query.all()
    if form.validate_on_submit():
        new_comment = Comment(comment = form.comment.data)
        new_comment.save()

        return redirect(url_for('main.comment'))
    return render_template('comments.html', form=form, comments=comments)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    uname = current_user.username
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template('profile/profile.html', user=user)


@main.route('/user/<uname>/update_profile', methods=['POST', 'GET'])
@login_required
def update_profile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/update.html', form=form, uname=uname)


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

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))