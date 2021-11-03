"""
Tests the adding custom category
"""
import unittest
from BaseCase import BaseCase

class TestAddCustomCategory(BaseCase):
    """
    Unit test for adding custom category
    """
    def test_add_custom_category(self):
        """
        Adding a custom category, reflects the new category in the list
        """
        custom_category = "books"
        self.user.add_category(custom_category, 1)
        raw_content = self.user.transactions.keys()
        categories = []
        for category in raw_content:
            categories.append(category)
        assert custom_category in categories


if __name__ == '__main__':
    unittest.main()
