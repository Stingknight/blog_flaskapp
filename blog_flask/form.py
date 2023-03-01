# Migrate(app,db)

###this methods is used to inherit some variables or data to base.html
# @app.context_processor
# def base():
#     form=SearchForm()
#     return dict(form=form)

# class LoginForm(FlaskForm):
#     username=StringField('Username ',validators=[DataRequired()])
#     password=PasswordField('Password',validators=[DataRequired()])
#     submit=SubmitField('Submit')

# class RegisterForm(FlaskForm):
#     username=StringField('Username ',validators=[DataRequired()])
#     password=PasswordField('Password',validators=[DataRequired()])
#     confirm_password=PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password','Password Must match!')])
#     submit=SubmitField('Submit')

#     def check_username(self,field):
#         if User.query.filter_by(username=field.data).first():

#             raise ValidationError('Sorry, that username is taken!')

# class SearchForm(FlaskForm):

#     searched=StringField('Searched',validators=[DataRequired()])
#     submit=SubmitField("Submit")

