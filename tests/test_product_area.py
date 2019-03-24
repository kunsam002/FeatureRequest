# feature_request/test_product_area.py

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

    def test_blank_product_areas_query(self):
        """
        Checks ProductArea object query from DB works properly
        """

        results = ProductAreaService.query.filter(ProductArea.name == "").all()
        self.assertEqual(results, [])

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
                "name": "works",
                "description": "Products relating works"
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
            ProductAreaService.create(**data)

        self.assertGreaterEqual(ProductAreaService.query.count(), 4)

    def test_product_area_query(self):
        """
        Checks Product Area object query from DB works properly
        """

        results = ProductAreaService.query.filter(ProductArea.code == "works").count()
        self.assertEqual(results, 1)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
