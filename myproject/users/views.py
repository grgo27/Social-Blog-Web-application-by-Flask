from flask import Blueprint, render_template, redirect, request, url_for, abort, flash
from myproject import db, login_manager
from myproject.models import User, BlogPost
from myproject.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from flask_login import login_required, login_user, logout_user, current_user
from myproject.users.picture_handler import add_profile_pic

users=Blueprint('users',__name__)

# REGISTER USER
@users.route('/register',methods=['GET','POST'])
def register():

    form=RegistrationForm()

    if form.validate_on_submit():

        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')

        return redirect(url_for('users.login'))
    
    return render_template('register.html',form=form)

# LOGIN USER
@users.route('/login',methods=['GET','POST'])
def login():

    form=LoginForm()

    if form.validate_on_submit():

        user=User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Login succesfull')

            next=request.args.get('next')

            if next==None or not next[0]=='/':
                next=url_for('core.index')
            
            return redirect(next)
        
    return render_template('login.html',form=form)

# LOGOUT USER
@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout succesfully')
    
    return redirect(url_for('core.index'))

# ACCOUNT (UPDATE USER)
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form=UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data: # ako smo loadali sliku
            username=current_user.username
            pic=add_profile_pic(form.picture.data, username)
            current_user.profile_image=pic
        
        current_user.username=form.username.data
        current_user.email=form.email.data

        db.session.commit()
        flash('User Account Updated!')

        return redirect(url_for('users.account'))
    
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    
    profile_image=url_for('static',filename='profile_pics/'+current_user.profile_image)
    
    return render_template('account.html',form=form,profile_image=profile_image)

# USER BLOG POST
@users.route('/<username>') # zahtjevamo username parametar 
def user_posts(username):
    page=request.args.get('page',1,type=int)

    user=User.query.filter_by(username=username).first_or_404()

    blog_posts=BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('user_blog_post.html',user=user,blog_posts=blog_posts)
        
# LIST OF REGISTER USERS
@users.route('/list_of_users')
def list_of_users():

    all_users=User.query.all()

    return render_template('users_list.html',all_users=all_users)

@users.route('/delete_user',methods=['GET','POST'])
@login_required
def delete_user():

    user=db.session.get(User,current_user.id)

    if user.posts:
        abort(406)
    
    db.session.delete(user)
        
    db.session.commit()

    return redirect(url_for('core.index'))




