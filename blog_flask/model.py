from . import db
from datetime import datetime
from flask_login import UserMixin
from . import bcrypt

class User(db.Model,UserMixin):

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    posts=db.relationship('Addpost',backref='poster')
    profile_pic=db.Column(db.String(),nullable=True)
    author_commenter=db.relationship('Comment',backref='commenter')

    def check_password(self,attempted_Password):

        return bcrypt.check_password_hash(self.password,attempted_Password)

    def __repr__(self):
      return f'{self.username,self.password,self.id}'



class Addpost(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50))
    #Author=db.Column(db.String(50))
    content=db.Column(db.Text(300))
    date_posted=db.Column(db.DateTime,default=datetime.utcnow)
    
    poster_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    post_comment=db.relationship('Comment',backref='postcommenter')

class Comment(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(500),nullable=True)
    post_id=db.Column(db.Integer,db.ForeignKey('addpost.id'))
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
