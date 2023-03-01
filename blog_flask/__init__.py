from flask import Flask,redirect,render_template,url_for,flash,session,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt

from datetime import datetime,date
import os

# from flask_wtf import FlaskForm
# from wtforms import StringField,SubmitField,IntegerField,PasswordField
# from wtforms.validators import Length,DataRequired,EqualTo,ValidationError
# from flask_wtf import FlaskForm
# from wtforms import StringField,SubmitField,SearchField
# from wtforms.validators import DataRequired
from flask_migrate import Migrate

app=Flask(__name__)


bcrypt=Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.sqlite'
app.config['SECRET_KEY']='hellouseer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)





from .blog_app import *