"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class User(db.Model):
    """User"""

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name}"

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default="https://help.salesforce.com/resource/1579912412000/HelpStaticResource/assets/images/tdxDefaultUserLogo.png")


class Post(db.Model):
    """Post"""

    def __repr__(self):
        return f"{self.id} {self.title} {self.user_id}"

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
