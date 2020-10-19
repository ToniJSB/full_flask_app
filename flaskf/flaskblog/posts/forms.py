from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l

class PostForm(FlaskForm):
    title = StringField(_('Title'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired()])
    submit = SubmitField(_('Create'))

