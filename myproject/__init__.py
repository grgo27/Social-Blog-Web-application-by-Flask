import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api   

#### APPLICATION SETUP ####
app=Flask(__name__)

app.config['SECRET_KEY']='mysecretkey'
api=Api(app)

#### DATABASE SETUP ####

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

Migrate(app,db)


#### LOGIN CONFIGURATION ####
login_manager=LoginManager()

login_manager.init_app(app)
login_manager.login_view='users.login'


#### IMPORT I REGISTER BLUEPRINTOVA ####
from myproject.core.views import core
from myproject.error_pages.handlers import error_pages
from myproject.users.views import users
from myproject.blog_posts.views import blog_posts



app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)