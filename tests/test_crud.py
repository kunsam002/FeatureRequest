# feature_request/test_crud.py

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

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
