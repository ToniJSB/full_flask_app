from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Toni Jimenez',
        'title': 'blog Title 1',
        'content': 'blog Content 1',
        'date_posted': '8 de octubre de 2020'
    },
    {
        'author': 'Pedro Jimenez',
        'title': 'blog Title 2',
        'content': 'blog Content 2',
        'date_posted': '8 de octubre de 2020'
    },
    {
        'author': 'Toni Noguera',
        'title': 'blog Title 3',
        'content': 'blog Content 3',
        'date_posted': '8 de octubre de 2020'
    },
]



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts, title = 'home')

@app.route('/about')
def about():
    return render_template('about.html', title= ' about')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f' account created for {user.username}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(' you have been loged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for(home))
    else:
        flash('login unsuccessful', 'warning')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')