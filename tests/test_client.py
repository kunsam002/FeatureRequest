# feature_request/test_client.py

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

    def test_blank_clients_query(self):
        """
        Checks Client object query from DB works properly
        """

        results = ClientService.query.filter(Client.name == "").all()
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
            },
            {
                "name": "Client Z",
                "phone": "+2348130107796",
                "email": "clientz@mailinator.com",
                "description": "Client Z top of the Aviation Sector"
            }
        ]

        for data in payload:
            ClientService.create(**data)

        self.assertGreaterEqual(ClientService.query.count(), 3)

    def test_client_query(self):
        """
        Checks Client object query from DB works properly
        """

        results = ClientService.query.filter(Client.slug == "client-a").count()
        self.assertGreaterEqual(results, 1)

    def test_client_update_change(self):
        """
        Tests Client Update method works properly
        """

        client = ClientService.query.filter(Client.slug == "client-a").first()
        new_email = "newly_updated_client_email@britecore.com"

        client = ClientService.update(client.id, email=new_email)

        self.assertEqual(client.email, new_email)

    def test_client_update(self):
        """
        Tests Client Update method works properly
        """

        client = ClientService.query.filter(Client.slug == "client-a").first()
        initial_email = client.email
        new_email = "newly_updated_testiniclient_email@britecore.com.ng"

        client = ClientService.update(client.id, email=new_email)

        self.assertNotEqual(client.email, initial_email)

    def test_client_delete(self):
        """
        Tests Client delete
        """

        data = {
            "name": "Client Z",
            "phone": "+2348130107796",
            "email": "clientz@mailinator.com",
            "description": "Client Z top of the Aviation Sector"
        }

        client = ClientService.create(**data)

        ClientService.delete(client.id)

        result = ClientService.query.filter(Client.slug == "client-z").count()

        self.assertEqual(result, 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
