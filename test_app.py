import unittest
from unittest import TestCase
from user import User
from bucketlist import BucketList
from flask import url_for, session

from app import app


class BucketListTest(TestCase):
    def setUp(self):        
        app.config['SECRET_KEY'] = 'seasasaskrit!'
        # creates a test client
        self.client = app.test_client()
        
        self.client.testing = True

    def test_success(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_failure(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.client.get('/nonexistant.html')
        self.assertEqual(result.status_code, 404)
    
    def test_login_page_loads(self):
        # assert login page loads correctly
        result = self.client.get('/login')
        self.assertTrue(b'The best way to keep track of your dreams and goals' in result.data)

    def test_sign_page_posts_and_redirects(self):
        result = self.client.post('signup', data={
            'username': 'hermano',
            'email': 'herm@email.com',
            'password': 'hard',
            'confirm_password': 'hard'
        })
        self.assertTrue(result.status_code == 302)

    

if __name__ == '__main__':
    unittest.main()
