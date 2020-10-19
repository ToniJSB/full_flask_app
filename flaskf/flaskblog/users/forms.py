from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User
from flask_babel import _, lazy_gettext as _l

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), Length(min=2,max = 20)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password  = PasswordField(_l('Password'), validators=[DataRequired()])
    confirm_password  = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Sign up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('this username is taken. You must choose a different one'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('this email is taken. You must choose a different one'))

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Login'))

class AccountForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), Length(min=2,max = 20)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    picture = FileField(_l('Update Profile Picture'), validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(_l('Update'))

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(_('this username is taken. You must choose a different one'))


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(_('this email is taken. You must choose a different one'))

class RequestResetForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(),Email()])

    submit = SubmitField(_l('Request Password Reset'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(_('There is no account with that email. You must register first.'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset Password'))