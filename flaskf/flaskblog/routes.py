from flask import render_template, flash, redirect, url_for
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f' account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(' you have been loged in!', 'success')
            return redirect(url_for('home'))
    else:
        flash('login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)
