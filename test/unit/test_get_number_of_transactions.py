from BaseCase import BaseCase
from datetime import datetime


class TestNumberOfTransactions(BaseCase):
    """
    Unit test for display_transaction
    """
    def test_get_none(self):
        """
        Given one category, we expect one row
        """
        assert self.user.get_number_of_transactions() == 0

    def test_get_one(self):
        """
        Given one category, we expect one row
        """
        # only 1 row
        date = datetime.today()
        self.user.transactions[self.user.spend_categories[0]].append({"Date": date, "Value": 10.00})
        assert self.user.get_number_of_transactions() == 1

    def test_get_two_cat(self):
        """
        Given multiple categories, it should have the
        categories on separate lines
        """
        # 2 rows
        date = datetime.today()
        self.user.transactions[self.user.spend_categories[0]].append({"Date": date, "Value": 10.00})
        self.user.transactions[self.user.spend_categories[1]].append({"Date": date, "Value": 15.00})
        assert self.user.get_number_of_transactions() == 2

    def test_get_same_cat(self):
        """
        Given multiple purchases in same category
        """
        # 2 rows
        date = datetime.today()
        self.user.transactions[self.user.spend_categories[0]].append({"Date": date, "Value": 10.00})
        self.user.transactions[self.user.spend_categories[0]].append({"Date": date, "Value": 15.00})
        assert self.user.get_number_of_transactions() == 2
