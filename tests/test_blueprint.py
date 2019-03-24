# feature_request/test_blueprint.py

import os
import unittest
from feature_request.services import *

db = app.db

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(app.config['BASE_DIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def test_index_page_data(self):
        """
        Checks to be sure that the index view function has all the arguments required for a proper page render
        """
        response = self.app.get('/?test=True', follow_redirects=True)

        required_response_args = ["title", "users_count", "requests_count", "clients_count", "is_unit_test"]
        argument_validator = all(key.encode() in response.data for key in required_response_args)

        self.assertTrue(argument_validator)

    def test_index_page(self):
        """
        Checks that the index page renders successfully
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_clients_page(self):
        """
        Checks that the clients page renders successfully
        """

        response = self.app.get('/clients/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_requests_page(self):
        """
        Checks that the requests page renders successfully
        """

        response = self.app.get('/requests/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_product_areas_page(self):
        """
        Checks that the product areas page renders successfully
        """

        response = self.app.get('/product_areas/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
