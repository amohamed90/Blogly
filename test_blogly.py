from app import app
from unittest import TestCase
from models import db, connect_db, User

app.config['TESTING'] = True

class BloglyTestCase(TestCase):
    """Testing routes for blogly app"""

    # def setUp(self):


    def test_home_page(self):
        with app.test_client() as client:

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('<h1>Users</h1>', html)
            self.assertEqual(resp.location, "http://localhost/users")

    def test_user_page(self):
        with app.test_client() as client:

            resp = client.post('/users/new', data={
                'first_name': 'Matt', 'last_name': 'Mike', 'image_url': 'http://www.google.com'
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Matt Mike', html)

    # def test_edit_page(self):
    # with app.test_client() as client:

    #     resp = client.post('/users/', data={
    #         'first_name': 'Matt', 'last_name': 'Mike', 'image_url': 'http://www.google.com'
    #     }, follow_redirects=True)
    #     html = resp.get_data(as_text=True)

    #     self.assertIn('Matt Mike', html)