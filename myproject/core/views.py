from flask import render_template, Blueprint, request
from myproject.models import BlogPost,User
from myproject import api
from flask_restful import Resource


core=Blueprint('core',__name__)

@core.route('/')
def index():
    page=request.args.get('page',1,type=int)

    blog_posts=BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('index.html',blog_posts=blog_posts)


@core.route('/info')
def info():

    return render_template('info.html')


class UserName(Resource):

    def get(self,username):
        user=User.query.filter_by(username=username).first()

        return user.json()
    
class AllUsers(Resource):

    def get(self):
        users=User.query.all()
        return [user.json() for user in users]

api.add_resource(UserName,'/users/<username>')
api.add_resource(AllUsers,'/all_users')