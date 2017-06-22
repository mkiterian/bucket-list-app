import unittest
from unittest import TestCase
from user import User
from bucketlist import BucketList
from flask import url_for

from app import app


class BucketListTest(TestCase):
    def setUp(self):
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
    '''
    def test_signup(self):
        # register a new account
        

            response = self.client.post(url_for('/signup'), data={
            'username': 'hermano',
            'email': 'herm@email.com',
            'password': 'hard',
            'confirm_password': 'hard'
            })
            self.assertTrue(response.status_code == 302)
    '''
    
    

if __name__ == '__main__':
    unittest.main()
