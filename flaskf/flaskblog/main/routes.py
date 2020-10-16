from flask import render_template, request, Blueprint, json
from flaskblog.models import Post
from flask import current_app
from flask_babel import gettext


main = Blueprint('main',__name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
    postsJson = Post.query.order_by(Post.date_posted.desc())
    js = []
    for post in postsJson:
        js.append(post.to_dict())
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    

        
    return render_template('home.html', posts = posts, json = js, title = 'home', languages=languages, locale=locale)

@main.route('/about')
def about():
    return render_template('about.html', title= ' about')
