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
                "name": "Works",
                "description": "Products relating works"
            },
            {
                "name": "Claims",
                "description": "Products relating claims"
            },
            {
                "name": "Reports",
                "description": "Products relating reports"
            },
            {
                "name": "Logistics",
                "description": "Products relating logistics"
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

    def test_product_area_change(self):
        """
        Tests Product Area Update method works properly
        """

        data = {
            "name": "Logistics",
            "description": "Products relating logistics"
        }

        product = ProductAreaService.create(**data)
        new_description = "All Of Logistics"

        product = ProductAreaService.update(product.code, description=new_description)

        self.assertEqual(product.description, new_description)

    def test_product_area_update(self):
        """
        Tests Product Area Update method works properly
        """

        data = {
            "name": "Logistics",
            "description": "Products relating logistics"
        }

        product = ProductAreaService.create(**data)
        initial_description = product.description
        new_description = "All Britecore related logistics"

        product = ProductAreaService.update(product.code, description=new_description)

        self.assertNotEqual(product.description, initial_description)

    def test_product_area_delete(self):
        """
        Tests Product Area delete
        """

        data = {
            "name": "Testing",
            "description": "Products relating testing"
        }

        product = ProductAreaService.create(**data)

        ProductAreaService.delete(product.code)

        result = ProductAreaService.query.filter(ProductArea.code == "testing").count()

        self.assertEqual(result, 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
