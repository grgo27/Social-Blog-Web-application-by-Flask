from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from myproject.models import User
from flask_login import current_user
from wtforms import ValidationError

class LoginForm(FlaskForm):

    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')


class RegistrationForm(FlaskForm):

    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Password must match!')])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Register')

    def validate_email(self,email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('That Email has already been registered')


    def validate_username(self,username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('That Username has already been registered')


class UpdateUserForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')


    def validate_email(self,email):
        user=User.query.filter_by(email=self.email.data).first()

        if user and user!=current_user:
            raise ValidationError('That Email has already been registered')
        

    def validate_username(self,username):
        user=User.query.filter_by(username=self.username.data).first()

        if user and user!=current_user:
            raise ValidationError('That Username has already been registered')
        


    

