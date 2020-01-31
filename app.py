"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "DHFGUSRGHUISHGUISHG"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.route('/')
def index():
    """Home Page"""

    return redirect('/users')


@app.route('/users')
def users():
    """Users Page"""

    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/users/new')
def add_user():
    """Add User Page"""

    return render_template('form.html')


@app.route('/users/new', methods=["POST"])
def add_user_form():
    """Add User Form Submit"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] if request.form["image_url"] else None


    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>')
def user_info(user_id):
    """User Info Page"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template('user-detail.html', user=user, posts=posts)


@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    """Edit User Page"""

    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)


@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user_form(user_id):
    """Edit User Form Submit"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"] if request.form["image_url"] else 'https://help.salesforce.com/resource/1579912412000/HelpStaticResource/assets/images/tdxDefaultUserLogo.png'

    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User Form Submit"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<user_id>/posts/new')
def add_post(user_id):
    """Add Post Form Submit"""

    user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)


@app.route('/users/<user_id>/posts/new', methods=["POST"])
def add_post_form(user_id):
    """Show Post Form Submit"""

    User.query.get_or_404(user_id)

    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title,
                    content=content,
                    user_id=int(user_id))

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):
    """Show Post"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post-detail.html', post=post, user=user)

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Edit Post"""

    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post_form(post_id):
    """Handling Edit Post-Form"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete Post Form Submit"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')