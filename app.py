"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "DHFGUSRGHUISHGUISHG"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
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
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>')
def user_info(user_id):
    """User Info Page"""

    user = User.query.get(user_id)
    return render_template('user-detail.html', user=user)


@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    """Edit User Page"""

    user = User.query.get(user_id)
    return render_template('user-edit.html', user=user)


@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user_form(user_id):
    """Edit User Form Submit"""

    user = User.query.get(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User Form Submit"""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
