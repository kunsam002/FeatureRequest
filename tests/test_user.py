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


    def test_user_update_change(self):
        """
        Tests User Update method works properly
        """
        user = UserService.query.filter(User.username == "test_user2841186890").first()
        if not user:
            user_data = dict(name="Test User", username="test_user2841186890", password="1234@Abcd",
                             email="test_user59y116682@mailinator.com")
            user = UserService.create(**user_data)
        new_name = "User Name"

        user = UserService.update(user.id, name=new_name)

        self.assertEqual(user.name, new_name)

    def test_user_update(self):
        """
        Tests User Update method works properly
        """

        user = UserService.query.filter(User.username == "test_user2841186890").first()
        if not user:
            user_data = dict(name="Test User", username="test_user2841186890", password="1234@Abcd",
                             email="test_user59y116682@mailinator.com")
            user = UserService.create(**user_data)

        initial_name = user.name
        new_name = "New Name"

        user = UserService.update(user.id, name=new_name)

        self.assertNotEqual(user.name, initial_name)

    def test_user_delete(self):
        """
        Tests User delete
        """

        user = UserService.query.filter(User.username == "test_user2841186890").first()

        UserService.delete(user.id)

        result = UserService.query.filter(User.username == "test_user2841186890").count()

        self.assertEqual(result, 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
