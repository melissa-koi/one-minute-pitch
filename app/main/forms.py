from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    title = StringField('title',validators=[Required()])
    comment = TextAreaField('comment', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    category = SelectField('Category', choices=[('Interview Pitch', 'Interview Pitch'), ('Sales Pitch', 'Sales Pitch'), ('Promotion Pitch', 'Promotion Pitch') , ('Pickup Lines', 'Pickup Lines') , ('Business Pitch', 'Business Pitch')],
                           validators=[Required()])
    post = TextAreaField('Pitch', validators=[Required()])
    author = StringField('Author', validators=[Required()])
    submit = SubmitField('Post')
