import unittest

from code.code import calculate_spendings


class TestCalculateSpendings(unittest.TestCase):
    """
    Unit test for calculate_spendings
    """

    def test_calculate_one_cat(self):
        """
        Given one category, we expect one row
        """
        # only 1 row
        query = ["d,c1,5"]
        expected_str = "c1 $5.00\n"
        assert calculate_spendings(query) == expected_str

    def test_calculate_two_cat(self):
        """
        Given multiple categories, it should have the
        categories on separate lines
        """
        query = ["d,c1,5", "d1,c2,2"]

        expected_str = "c1 $5.00\nc2 $2.00\n"
        assert calculate_spendings(query) == expected_str

    def test_calculate_multiple_row(self):
        """
        Given multiple purchases in same category,
        it should sum them
        """
        query = ["d,c1,5", "d1,c2,2", "d1,c1,15"]

        expected_str = "c1 $20.00\nc2 $2.00\n"
        assert calculate_spendings(query) == expected_str

    def test_calculate_spending_multiple_all(self):
        """
        Given multiple categories with multiple spending's,
        should sum per each category
        """
        query = ["d,c1,5", "d1,c2,2", "d1,c1,15", "d1,c2,35"]

        expected_str = "c1 $20.00\nc2 $37.00\n"
        assert calculate_spendings(query) == expected_str
