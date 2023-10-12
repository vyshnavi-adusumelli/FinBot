import unittest
from discord_BaseCase import discord_BaseCase
from datetime import datetime, timedelta


class TestAddUserRecord(discord_BaseCase):
    """
        Tests the edit series of functions in bot.py
    """

    def test_store_edit_transaction(self):
        """
        After user enters existing transaction and data is parsed from input
        user.edit_transaction should be that transaction
        user.edit_category should be the category of that transaction
        """
        # User enters the following date,category, value
        user_date = datetime.today()
        user_category = "Food"
        user_value = 10.00
        userid = "2"
        self.user.add_transaction(user_date, user_category, user_value, userid)
        transaction = {"Date": user_date, "Value": user_value}
        self.user.store_edit_transaction(transaction, user_category)
        assert transaction == self.user.edit_transactions
        assert user_category == self.user.edit_category

    def test_edit_date(self):
        # User enters the following date,category, value
        user_date = datetime.today()
        edit_date = datetime.today() - timedelta(days=1)
        user_category = "Groceries"
        user_value = 10.00
        userid = "2"
        self.user.add_transaction(user_date, user_category, user_value, userid)
        transaction = {"Date": user_date, "Value": user_value}
        self.user.store_edit_transaction(transaction, user_category)
        self.user.edit_transaction_date(edit_date)
        assert self.user.transactions["Groceries"][0]["Date"].date() == edit_date.date()

    def test_edit_transaction_category(self):
        # User enters the following date,category, value
        user_date = datetime.today()
        user_category = "Utilities"
        edit_category = "Transport"
        user_value = 10.00
        userid = "2"
        self.user.add_transaction(user_date, user_category, user_value, userid)
        transaction = {"Date": user_date, "Value": user_value}
        self.user.store_edit_transaction(transaction, user_category)
        self.user.edit_transaction_category(edit_category)
        assert self.user.transactions[edit_category][0] == transaction

    def test_edit_transaction_value(self):
        # User enters the following date,category, value
        user_date = datetime.today()
        user_category = "Shopping"
        user_value = 10.00
        edit_value = 20.00
        userid = "2"
        self.user.add_transaction(user_date, user_category, user_value, userid)
        transaction = {"Date": user_date, "Value": user_value}
        self.user.store_edit_transaction(transaction, user_category)
        self.user.edit_transaction_value(edit_value)
        assert self.user.transactions["Shopping"][0]["Value"] == edit_value
