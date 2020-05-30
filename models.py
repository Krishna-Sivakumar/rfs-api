from flask_sqlalchemy import SQLAlchemy
import json
import datetime
from hashlib import sha256

db = SQLAlchemy()

class Board(db.Model):
    # Relations
    threads = db.relationship('Thread', backref = 'board')

    # Data
    board_name = db.Column(db.Text, primary_key = True)
    description = db.Column(db.Text)

    def to_json(self):
        return json.dumps({
            'name': self.board_name,
            'description': self.description,
        })


class User(db.Model):
    # Relations
    user_email = db.Column(db.String(60), primary_key = True)
    threads = db.relationship('Thread', backref='user')
    comments = db.relationship('Comment', backref='user')

    # Data

    username = db.Column(db.Text, nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)
    description = db.Column(db.Text)
    deleted = db.Column(db.Boolean, default = False)
    time_created = db.Column(db.Date, nullable=False, default = datetime.datetime.now().date())

    def to_json(self):
        # Returns a json string representing an User object
        return json.dumps({
            'username': self.username,
            'user_email': self.user_email,
            'description': self.description,
            'deleted': self.deleted
        })

    def set_password(self, password):
        self.password_hash = sha256(password.encode('utf-8')).digest()

    def check_password(self, password):
        return self.password_hash == sha256(password.encode('utf-8')).digest()

    def __repr__(self):
        return self.toJSON()

class Thread(db.Model):
    # Relations
    thread_id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.Integer, db.ForeignKey('user.user_email'), nullable = False)
    board_name = db.Column(db.Integer, db.ForeignKey('board.board_name'), nullable = False)
    comments = db.relationship('Comment', backref = 'Thread')
    
    # Data
    name = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    deleted = db.Column(db.Boolean, default = False)
    timeCreated = db.Column(db.Date, nullable = False, default = datetime.datetime.now().date())

    def to_json(self):
        return json.dumps({
            'thread_id': self.thread_id,
            'user_email': self.user_email,
            'board_name': self.board_name,
            'comments': [comment.to_json() for comment in self.comments],
            'name': self.name,
            'content': self.content,
            'deleted': self.deleted
        })


class Comment(db.Model):
    # Relations
    comment_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.Integer, db.ForeignKey('user.user_email'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.thread_id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'))

    parent = db.relationship('Comment', remote_side = [comment_id], backref = 'children')

    # Data
    deleted = db.Column(db.Boolean, default = False)
    content = db.Column(db.Text)
    timeCreated = db.Column(db.Date, nullable=False, default = datetime.datetime.now().date())

    def to_json(self):
        return json.dumps({
            'comment_id': self.comment_id,
            'user_email': self.user_email,
            'thread_id': self.thread_id,
            'parent_id': self.parent_id,
            'deleted': self.deleted,
            'content': self.content,
        })
