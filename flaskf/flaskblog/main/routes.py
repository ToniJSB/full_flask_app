from flask import render_template, request, Blueprint, json
from flaskblog.models import Post


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
    
    return render_template('home.html', posts = posts, json = js, title = 'home')

@main.route('/about')
def about():
    return render_template('about.html', title= ' about')
