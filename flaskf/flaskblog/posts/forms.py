from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_babel import gettext

class PostForm(FlaskForm):
    title = StringField(gettext(u'Title'), validators=[DataRequired()])
    content = TextAreaField(gettext(u'Content'), validators=[DataRequired()])
    submit = SubmitField(gettext(u'Create'))

