# feature_request/test_basic.py

import os
import unittest
import json

from flask import session
from feature_request import app
from feature_request.services import *

db = app.db

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
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

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_user_query(self):
        """
        Checks User object query from DB qorks properly
        """
        results = UserService.query.filter(User.username == "").all()
        self.assertEqual(results, [])

    def test_clients_query(self):
        """
        Checks Client object query from DB qorks properly
        """

        results = ClientService.query.filter(Client.name == "").all()
        self.assertEqual(results, [])

    def test_product_areas_query(self):
        """
        Checks ProductArea object query from DB qorks properly
        """

        results = ProductAreaService.query.filter(ProductArea.name == "").all()
        self.assertEqual(results, [])

    def test_client_creation(self):
        """
        Checks Client object creation and record saves properly to the Database
        """

        payload = [
            {
                "name": "Client A",
                "phone": "+2348130107796",
                "email": "clienta@mailinator.com",
                "description": "Client A top of the Aviation Sector"
            },
            {
                "name": "Client B",
                "phone": "+2347046399814",
                "email": "clientb@mailinator.com",
                "description": "Client B top of the Transport Sector"
            },
            {
                "name": "Client C",
                "phone": "+2348130107796",
                "email": "clientc@mailinator.com",
                "description": "Client C top of the Aviation Sector"
            }
        ]

        for data in payload:
            client = ClientService.create(**data)

        self.assertGreaterEqual(ClientService.query.count(), 3)

    def test_product_area_creation(self):
        """
        Checks ProductArea object creation and record saves properly to the Database
        """

        payload = [
            {
                "name": "Policies",
                "description": "Products relating policies"
            },
            {
                "name": "Billing",
                "description": "Products relating billing"
            },
            {
                "name": "Claims",
                "description": "Products relating claims"
            },
            {
                "name": "Reports",
                "description": "Products relating reports"
            }
        ]

        for data in payload:
            product_area = ProductAreaService.create(**data)

        self.assertGreaterEqual(ProductAreaService.query.count(), 4)

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


if __name__ == "__main__":
    unittest.main()
