from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, AccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email
from flask_babel import gettext


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(gettext(u' account created for %(user)%!',user=user.username), 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, languages=languages, locale=locale)

@users.route('/login', methods=['GET','POST'])
def login():
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(gettext(u'you have been loged in!'), 'success')
            if next_page:
                return redirect(next_page)
            else :
                return redirect(url_for('main.home'))
    else:
        flash(gettext(u'login unsuccessful'), 'warning')
    return render_template('login.html', title='Login', form=form,languages=languages, locale=locale)

@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = AccountForm()
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(gettext(u'Your account has been updated!'), 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= 'profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, languages=languages, locale=locale)

@users.route('/user/<string:username>')
def user_posts(username):
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_post.html', posts = posts, user= user, languages=languages, locale=locale)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(gettext(u'An email has been sent with instructions to reset your password.'), 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form, languages=languages, locale=locale)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(gettext(u'That is an invalid or expired token'), 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(gettext(u'Your password has been updated! You are now able to log in'), 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form, languages=languages, locale=locale)