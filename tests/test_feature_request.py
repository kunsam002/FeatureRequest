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

    def test_request_update_change(self):
        """
        Tests Feature Request Update method works properly
        """
        data = {
            "title": "QA Review",
            "description": "There is a need for QA review on the Billing section of the product",
            "client_id": 1,
            "client_priority": 4,
            "target_date": datetime.today() + timedelta(hours=78),
            "product_area_code": "billing",
            "user_id": 1
        }
        obj = FeatureRequestService.create(**data)
        new_priority = 100

        obj = FeatureRequestService.update(obj.id, client_priority=new_priority)

        self.assertEqual(obj.client_priority, new_priority)

    def test_request_update(self):
        """
        Tests Feature Request Update method works properly
        """

        data = {
            "title": "QA Review",
            "description": "There is a need for QA review on the Billing section of the product",
            "client_id": 1,
            "client_priority": 4,
            "target_date": datetime.today() + timedelta(hours=78),
            "product_area_code": "billing",
            "user_id": 1
        }
        obj = FeatureRequestService.create(**data)
        new_priority = 180
        initial_priority = obj.client_priority

        obj = FeatureRequestService.update(obj.id, client_priority=new_priority)

        self.assertNotEqual(obj.client_priority, initial_priority)

    def test_request_delete(self):
        """
        Tests Client delete
        """

        data = {
            "title": "QA Review",
            "description": "There is a need for QA review on the Billing section of the product",
            "client_id": 1,
            "client_priority": 4,
            "target_date": datetime.today() + timedelta(hours=78),
            "product_area_code": "billing",
            "user_id": 1
        }
        obj = FeatureRequestService.create(**data)

        obj_id = obj.id

        FeatureRequestService.delete(obj_id)

        result = FeatureRequestService.query.filter(FeatureRequest.id == obj_id).count()

        self.assertEqual(result, 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
