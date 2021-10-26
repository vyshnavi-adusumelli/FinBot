import unittest
from BaseCase import BaseCase
from datetime import datetime


class TestAddUserRecord(BaseCase):
    """
        Tests the edit series of functions in bot.py
    """
    def add_new_transaction(self):
        date = datetime.today()
        category = "Food"
        value = 10.00
        userid = "3333333"
        self.user.add_transaction(date, category, value, userid)

    def test_edit_date(self):


    def test_edit_cat(self):
        pass

    def test_edit_cost(self):
        pass


