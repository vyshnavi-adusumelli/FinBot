from discord_BaseCase import discord_BaseCase
from datetime import datetime


class TestDisplayTransaction(discord_BaseCase):
    """
    Unit test for display_transaction
    """

    def test_display_one_cat(self):
        """
        Given one category, we expect one row
        """
        # only 1 row
        date = datetime.today()
        transaction = {self.user.spend_categories[0]: [{"Date": date, "Value": 10.0}]}
        expected_str = f'{self.user.spend_categories[0]}, {date.date()}, 10.0\n'
        assert self.user.display_transaction(transaction) == expected_str

    def test_display_two_cat(self):
        """
        Given multiple categories, it should have the
        categories on separate lines
        """
        # 2 rows
        date = datetime.today()
        transaction = {self.user.spend_categories[0]: [{"Date": date, "Value": 10.0}],
                       self.user.spend_categories[1]: [{"Date": date, "Value": 15.0}]}
        expected_str = f'{self.user.spend_categories[0]}, {date.date()}, 10.0\n' \
                       f'{self.user.spend_categories[1]}, {date.date()}, 15.0\n'
        assert self.user.display_transaction(transaction) == expected_str

    def test_display_multiple_row(self):
        """
        Given multiple purchases in same category
        """
        date = datetime.today()
        transaction = {self.user.spend_categories[0]: [{"Date": date, "Value": 10.0},
                                                       {"Date": date, "Value": 15.0}]}
        expected_str = f'{self.user.spend_categories[0]}, {date.date()}, 10.0\n' \
                       f'{self.user.spend_categories[0]}, {date.date()}, 15.0\n'
        assert self.user.display_transaction(transaction) == expected_str

    def test_display_spending_multiple_all(self):
        """
        Given multiple categories with multiple spending's
        """
        date = datetime.today()
        transaction = {self.user.spend_categories[0]: [{"Date": date, "Value": 10.0},
                                                       {"Date": date, "Value": 15.0}],
                       self.user.spend_categories[1]: [{"Date": date, "Value": 5}]}
        expected_str = f'{self.user.spend_categories[0]}, {date.date()}, 10.0\n' \
                       f'{self.user.spend_categories[0]}, {date.date()}, 15.0\n' \
                       f'{self.user.spend_categories[1]}, {date.date()}, 5\n'
        ret = self.user.display_transaction(transaction)
        assert ret == expected_str
