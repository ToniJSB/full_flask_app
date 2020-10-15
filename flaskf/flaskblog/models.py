from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin, SerializerMixin):


    serialize_only = ('id', 'username', 'email','img_file')

    serialize_rules = ('-password')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post',back_populates='author', lazy=True)

    def get_reset_token(self,expires_sec=4000):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    @property
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'img_file' : self.img_file,
        }


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"

class Post(db.Model, SerializerMixin):

    serialize_only = ('id', 'title', 'date_posted','content', 'author.username', 'author.id', 'author.username', 'author.img_file')


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User',back_populates='posts')
    @property
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_posted' : self.date_posted,
            'content' : self.content,
            'author' : self.user_id  
        }

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
