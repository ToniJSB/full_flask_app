from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User
from flask_babel import gettext

class RegistrationForm(FlaskForm):
    username = StringField(gettext(u'Usuario'), validators=[DataRequired(), Length(min=2,max = 20)])
    email = StringField(gettext(u'Email'), validators=[DataRequired(), Email()])
    password  = PasswordField(gettext(u'Password'), validators=[DataRequired()])
    confirm_password  = PasswordField(gettext(u'Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(gettext(u'Sign up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(gettext(u'this username is taken. You must choose a different one'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(gettext(u'this email is taken. You must choose a different one'))

class LoginForm(FlaskForm):
    email = StringField(gettext(u'Email'), validators=[DataRequired(), Email()])
    password = PasswordField(gettext(u'Password'), validators=[DataRequired()])
    remember = BooleanField(gettext(u'Remember me'))
    submit = SubmitField(gettext(u'Login'))

class AccountForm(FlaskForm):
    username = StringField(gettext(u'Username'), validators=[DataRequired(), Length(min=2,max = 20)])
    email = StringField(gettext(u'Email'), validators=[DataRequired(), Email()])
    picture = FileField(gettext(u'Update Profile Picture'), validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(gettext(u'Update'))

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(gettext(u'this username is taken. You must choose a different one'))


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(gettext(u'this email is taken. You must choose a different one'))

class RequestResetForm(FlaskForm):
    email = StringField(gettext(u'Email'), validators=[DataRequired(),Email()])

    submit = SubmitField(gettext(u'Request Password Reset'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(gettext(u'There is no account with that email. You must register first.'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(gettext(u'Password'), validators=[DataRequired()])
    confirm_password = PasswordField(gettext(u'Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(gettext(u'Reset Password'))