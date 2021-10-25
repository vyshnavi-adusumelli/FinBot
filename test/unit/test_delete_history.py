"""
Test for the deleteHistory function
"""

from datetime import datetime
from BaseCase import BaseCase


class TestDeleteHistory(BaseCase):
    """
    Unit test for deleteHistory
    """



    def test_delete_history_none(self):
        """
        Given no transactions, the list should not change
        """
        # given no history
        assert self.user.get_number_of_transactions() == 0
        # doing deleteHistory
        self.user.deleteHistory()
        # should not do anything
        assert self.user.get_number_of_transactions() == 0

    def test_delete(self):
        """
        Given there is one user
        deleting a transaction
        should remove it
        """
        # given adding one user
        date = datetime.today()
        transaction = self.create_transaction()
        record = {"Date": date, "Value": 10.00}
        transaction[self.user.spend_categories[0]].append(record)
        self.user.transactions[self.user.spend_categories[0]].append(record)
        # delete the transaction
        self.user.deleteHistory(transaction)
        assert self.user.get_number_of_transactions() == 0
        assert self.user.transactions[self.user.spend_categories[0]] == []

    def test_delete_multiple(self):
        """
        Given there is multiple transactions
        deleting one should work
        """
        # given adding one user
        date = datetime.today()
        transaction = self.create_transaction()
        record = {"Date": date, "Value": 10.00}
        # appending the transaction
        self.user.transactions[self.user.spend_categories[0]].append(record)
        # creating a record to delete
        to_delete = {"Date": date, "Value": 15.00}
        transaction[self.user.spend_categories[0]].append(to_delete)
        self.user.transactions[self.user.spend_categories[0]].append(to_delete)
        # delete the transaction
        self.user.deleteHistory(transaction)
        assert self.user.get_number_of_transactions() == 1
        assert self.user.transactions[self.user.spend_categories[0]] == [record]


    def test_delete_multiple_record(self):
        """
        Given there is one user
        deleting one record from the user
        should remove it from the user list
        """
        # given adding one user
        date = datetime.today()
        transaction = self.create_transaction()
        record = {"Date": date, "Value": 10.00}
        # appending the transaction
        self.user.transactions[self.user.spend_categories[0]].append(record)
        # creating a record to delete
        to_delete = {"Date": date, "Value": 15.00}
        transaction[self.user.spend_categories[0]].append(to_delete)
        self.user.transactions[self.user.spend_categories[0]].append(to_delete)
        # delete the transaction
        self.user.deleteHistory(transaction)
        assert self.user.get_number_of_transactions() == 1
        assert self.user.transactions[self.user.spend_categories[0]] == [record]

        # delete the last record
        transaction = self.create_transaction()
        transaction[self.user.spend_categories[0]].append(to_delete)
        self.user.deleteHistory(transaction)
        assert self.user.get_number_of_transactions() == 0
        assert self.user.transactions[self.user.spend_categories[0]] == []
