import unittest
from unittest import TestCase
from user import User

from bucket_list_app import app


class BucketListTest(TestCase):
    def setUp(self):
        # super(BucketListTest, self).setUp()
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        user = User 

    def test_success(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/bucketlist.html')
        self.assertEqual(result.status_code, 200)

    def test_failure(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/nonexistant.html')
        self.assertEqual(result.status_code, 404)

    def test_sign_up(self):
        #checks if sign up successfully adds new user
        pass

    

if __name__ == '__main__':
    unittest.main()
