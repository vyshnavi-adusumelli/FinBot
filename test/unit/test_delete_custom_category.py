"""
Tests the delete of custom category
"""
import unittest
from BaseCase import BaseCase

class TestDeleteCustomCategory(BaseCase):
    """
    Unit test for deleting custom category
    """
    def test_delete_custom_category(self):
        """
        Deleting a custom category, the custom category then does not reflect in the category list
        """

        custom_category = "books"
        self.user.add_category(custom_category, 1)
        raw_content = self.user.transactions.keys()
        categories = []
        for category in raw_content:
            categories.append(category)
        assert custom_category in categories

        self.user.delete_category(custom_category, 1)
        content = self.user.transactions.keys()
        categories = []
        for category in content:
            categories.append(category)
        assert custom_category not in categories

if __name__ == '__main__':
    unittest.main()
