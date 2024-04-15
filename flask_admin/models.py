from config import db
from flask_login import UserMixin

class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    birthday = db.Column(db.DateTime, unique=False, nullable=False)
    comments = db.relationship('Comment', backref='admins', lazy='dynamic')

    def __repr__(self):
        return '<Admins %r>' % (self.username)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.id)