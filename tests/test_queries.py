# feature_request/test_queries.py

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

    def tearDown(self):
        self.app = app.test_client()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()
