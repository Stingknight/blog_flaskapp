from . import app,redirect,render_template,jsonify,request,bcrypt
from .model import User,Comment,Addpost
from . import db,session,url_for,flash
from werkzeug.utils import secure_filename
import uuid 
import os
from flask_login import LoginManager,login_required,login_user,logout_user,current_user

UPLOAD_FOLDER='blog_flask/static/images'
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    
    return render_template('base.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':

        username=request.form['username1']
        password=request.form['password1']
        
        user=User.query.filter_by(username=username).first()
        
        if user :
            if bcrypt.check_password_hash(user.password,password):
            # (method2 to check password)if user.check_password(attempted_password=form.password.data):
            #This function will register the user as logged in, so that means that any future pages the user navigates to will have the current_user variable set to that user
                login_user(user)
                session['user']=username
                return redirect(url_for('dashboard'))
            else:
                flash('Password is wrong')

        else:
            flash('Username doesnot exist!!')
    return render_template('login.html')

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user=current_user
    if request.method=="POST":

        user_id=user.id
        data1=User.query.get(user_id)
        # username=session['user']
        
        image=request.files['picture']
        if image:
            pic_file_name=secure_filename(image.filename)
            pic_name=str(uuid.uuid1()) + "_" +pic_file_name
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
            
            data1.profile_pic=pic_name
            db.session.add(data1)
            db.session.commit()
        
        flash('Updated_sucessfully')
        return render_template('dashboard.html',user=user)
    
    return render_template('dashboard.html',user=user)
    

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    session.pop('user', None)
    logout_user()
    flash('You logged out!')
    return redirect(url_for('login'))


# @app.route('/market',methods=['GET','POST'])
# @login_required
# def market():
#     if 'user' in session:
        
#         username=session['user']
#         user=User.query.filter_by(username=username).first()
        
#         return render_template('market.html',user=user)
#     else:
#         return '<h3>Not logged in</h3>'

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':

        username=request.form['username']
        password=request.form['password']
        conf_password=request.form['conf_password']

        user=User.query.filter_by(username=username).first()
        
        
        if user :
            flash('username already exists!!')
        
        else:
            if password:
                if password==conf_password:
                    hashed_password=bcrypt.generate_password_hash(password)
                    user=User(username=username,
                        password=hashed_password)
                    db.session.add(user)
                    db.session.commit()
                    flash('Sucessfuly registerd')
                else:
                    flash('Password doesnot match')
            else:
                flash('Please fill username and enter password')
    return render_template('register.html')



# @app.route('/change_password_user',methods=['GET','POST'])

# @login_required
# def change_password_user():
#     if request.method=='POST':
   
#         user=session['user']
#         user1=current_user.username
#         old_password=request.form['password2']
#         new_password=request.form['password3']
#         username=User.query.filter_by(username=user1).first()
#         if username:
#             if bcrypt.check_password_hash(username.password,old_password):

#                 if new_password:
#                     update_password=User.query.get(username.id)
#                     hashed_password=bcrypt.generate_password_hash(new_password)
#                     update_password.password=hashed_password
                  
#                     db.session.add(update_password)
                   
#                     db.session.commit()
                      

#                     flash('Sucessfully changed password')
#                 else:
#                     flash('Enter the new password')
#             else:
#                 flash('Enter correct password')
      
#         return render_template('password.html')
            
#     return render_template('password.html')


@app.route('/add_post',methods=['GET','POST'])
@login_required
def addpost():
    if request.method=='POST':
        poster=current_user.id
        print(poster)
        title=request.form['title']
        #author=request.form['author']
        content=request.form['content']
        if title or content:

            data_post=Addpost(title=title,poster_id=poster,content=content)
            db.session.add(data_post)
            db.session.commit()
            

    return render_template('addpost.html')

@app.route('/Show_blogpost')
@login_required
def show_blog():

    posts=Addpost.query.order_by(Addpost.date_posted)
    comments=Comment.query.order_by(Comment.id)
    return render_template('showblog.html',posts=posts,comments=comments)
    
@app.route('/single_post')
def s_post():
    data_id=request.args['id_data']
    post=Addpost.query.get(data_id)
    return render_template('posts.html',post=post)


@app.route('/post/edit/<int:id>',methods=['GET','POST'])

def update(id):
    data=Addpost.query.get(id)
    if request.method=="POST":

        current=current_user.id
       
        if current==data.poster.id:
            data.title=request.form['title1']
            #data.Author=request.form['author1']
            data.content=request.form['content1']
            db.session.add(data)
            db.session.commit()
            flash('Updated sucessfully')
            return redirect(url_for('show_blog'))
        
        else:
            flash('only user can edit the profile')
       
    return render_template('update.html',id=id,data=data)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_post(id):
    current=current_user.id
    admin=User.query.get(1)
    
    data=Addpost.query.get(id)

    if current==data.poster.id or admin.id==1:
        db.session.delete(data)
        db.session.commit()
        flash('Deleted Sucessfully')
        
    else:
        flash('Only user can delete post')
    return redirect(url_for('show_blog'))

@app.route('/delete_user')
@login_required
def delete_user():
    id=current_user.id

    data=User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash('Your account is deleted sucessfully ')
    return redirect(url_for('register'))


#############this url is used using flask form

# @app.route('/search',methods=['POST'])
# def search():
    
#     form=SearchForm()

#     if form.validate_on_submit():
#         searched=form.searched.data

#         return render_template('search.html',form=form,searched=searched)
#     return render_template('search.html')



#only for admin page

@app.route('/admin')
@login_required
def admin():
    user=current_user.username
    if user=='adithya1':

        return render_template('admin.html')
    else:
        flash("You can't acess admin page")
        return redirect(url_for('dashboard'))
        
@app.route('/update_user')
def update_user():


    return render_template('update_user.html')

@app.route('/add_comments/<int:id>',methods=['GET','POST'])
@login_required
def add_comments(id):
    user=current_user.id
    if request.method=='POST':

        texts=request.form['comment']
        if texts:
            comment_data=Comment(text=texts,post_id=id,author_id=user)
            db.session.add(comment_data)
            db.session.commit()
            flash('sucessfully commented')
            return redirect (url_for('show_blog'))
        else:
            flash('please comment something')
            return redirect (url_for('show_blog'))
    return render_template('showblog.html')



@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=="POST":
        
        #post=Addpost.query
        searched=request.form['searched']
        if searched:
            post_data=Addpost.query.filter(Addpost.content.like('%' +searched+ '%'))
            post_filter=post_data.order_by(Addpost.title).all()
            return render_template('search.html',searched=searched,post_filter=post_filter)
    return render_template('search.html')


@app.route('/edit_comment',methods=['GET','POST'])
def edit_comment():
    user=current_user.id
    comment_id=request.form.get('comment_id')
    comment_data=Comment.query.get(comment_id)
    if user==comment_data.commenter.id:
        comment_data.text=request.form.get('comments')
        db.session.add(comment_data)
        db.session.commit()
        
        flash('updated comment sucessfully')
        return jsonify({'data':'data'})
       
            
   


@app.route('/delete_comments')
def delete_comments():
    user=current_user.id
    comment_id=request.args['comment']
    comment_data=Comment.query.get(comment_id)
    if user==comment_data.commenter.id:
        db.session.delete(comment_data)
        db.session.commit()
        flash('Comment deleted sucesfully')
        return redirect(url_for('show_blog'))
