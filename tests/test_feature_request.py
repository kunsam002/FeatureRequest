# feature_request/test_feature_request.py

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

    def test_blank_feature_request_query(self):
        """
        Checks Feature Request object query from DB works properly
        """

        results = FeatureRequestService.query.filter(FeatureRequest.title == "").all()
        self.assertEqual(results, [])

    def test_request_creation(self):
        """
        Checks Request object creation and record saves properly to the Database
        """

        payload = [
            {
                "title": "QA Review",
                "description": "There is a need for QA review on the Billing section of the product",
                "client_id": 1,
                "client_priority": 4,
                "target_date": datetime.today() + timedelta(hours=78),
                "product_area_code": "billing",
                "user_id": 1
            }
        ]

        for data in payload:
            FeatureRequestService.create(**data)

        self.assertGreaterEqual(FeatureRequestService.query.count(), 1)


    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
