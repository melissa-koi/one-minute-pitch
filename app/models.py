from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique=True,)
    email = db.Column(db.String(255), unique=True, index=True)
    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model, UserMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post = db.Column(db.Text, nullable=False)
    comment = db.relationship('Comment', backref='post', lazy='dynamic')
    category = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String)
   # liked = db.relationship('PostLike',foreign_keys='PostLike.users_id',backref='posts', lazy='dynamic')


    def like_post(self, post):
        if not self.has_liked_post(post):
            like = postLike(users_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            postLike.query.filter_by(
                users_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return postLike.query.filter(
            postLike.users_id == self.id,
            postLike.post_id == post.id).count() > 0

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Post Title: {self.title}"

# class PostLike(db.Model):
#     __tablename__ = 'post_like'
#     id = db.Column(db.Integer, primary_key=True)
#     users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment = db.Column(db.Text(), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comments: {self.comment}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
