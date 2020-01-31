from app import app
from unittest import TestCase
from models import db, connect_db, User, Post

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'


class BloglyTestCase(TestCase):
    """Testing routes for blogly app"""

    def setUp(self):
        user1 = User(first_name="DELETE DELETE DELETE", last_name="DIFF")
        db.session.add(user1)

        db.session.commit()

        post1a = Post(title="REMOVE POST", content="This is a post!", user_id=user1.id)
        db.session.add(post1a)

        db.session.commit()

        self.user = user1
        self.post = post1a


    def tearDown(self):

        db.session.delete(self.post)
        db.session.delete(self.user)

        db.session.commit()

    def test_home_page(self):
        with app.test_client() as client:

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.location, "http://localhost/users")

    def test_add_user(self):
        with app.test_client() as client:

            resp = client.post('/users/new', data={
                'first_name': 'DELETE-THIS-NAME', 'last_name': 'Mike', 'image_url': 'http://www.google.com'
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('DELETE-THIS-NAME', html)
            # TODO figure out why get is not working (can't bind user to session)
            user1 = User.query.filter_by(first_name="DELETE-THIS-NAME").first()

            db.session.delete(user1)

            db.session.commit()


    def test_edit_user(self):
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user.id}/edit', data={
                    'first_name': 'DELETE-THIS-NAME', 'last_name': 'Mike', 'image_url': 'http://www.google.com'
                }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertIn('DELETE-THIS-NAME', html)



    def test_delete_user(self):
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user.id}/delete', follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertNotIn("DELETE DELETE DELETE", html)

    def test_add_post(self):
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user.id}/posts/new', data={
                'title': 'HELLO WORLD', 'content': 'PLEASE WORK'
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertIn('HELLO WORLD', html)
            post1 = Post.query.filter_by(title="HELLO WORLD").first()

            db.session.delete(post1)

            db.session.commit()

    def test_delete_post(self):
        with app.test_client() as client:

            resp = client.post(f'/posts/{self.post.id}/delete', follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertNotIn("REMOVE POST", html)

    def test_edit_post(self):
        with app.test_client() as client:

            resp = client.post(f'/posts/{self.post.id}/edit', data={
                    'title': 'EDIT-THIS-POST', 'content': 'PLEASE'
                }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertIn('EDIT-THIS-POST', html)


