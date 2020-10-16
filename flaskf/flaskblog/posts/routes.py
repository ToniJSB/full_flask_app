
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts',__name__)


@posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash(gettext(u'your post has been created!'), 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New post', languages=languages, locale=locale)


@posts.route('/post/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, languages=languages, locale=locale)


@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    languages = current_app.config['LANGUAGES']
    locale = list(languages)[0]
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title =form.title.data
        post.content =form.content.data 
        db.session.commit()
        flash(gettext(u'your post has been updated!'),'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

        
    return render_template('create_post.html', title=gettext(u'Update Post'), form=form, legend=gettext(u'Update post'),languages=languages, locale=locale)

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(gettext(u'Your post has been deleted!'), 'success')
    return redirect(url_for('main.home'))
