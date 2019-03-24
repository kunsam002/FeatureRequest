# feature_request/test_user.py

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


    def test_blank_user_query(self):
        """
        Checks User object query from DB works properly
        """
        results = UserService.query.filter(User.username == "").all()
        self.assertEqual(results, [])


    def test_user_creation(self):
        """
        Checks User object creation and record saves properly to the Database
        """

        user_data = dict(name="Test User", username="testuser28869", password="1234@Abcd",
                         email="testuser59y62@mailinator.com")
        UserService.create(**user_data)

        self.assertEqual(UserService.query.filter(User.username=="testuser289").count(), 1)



    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
