from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):

    title=StringField('Title',validators=[DataRequired()])
    text=TextAreaField('Text',validators=[DataRequired()])
    submit=SubmitField('Post')
    # necu kreirat polje za user_id jer ce user trebat bit logiran da bi mogao kreirat postove i onda cu sa current_user dohvatit id