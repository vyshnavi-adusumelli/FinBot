import os.path
import unittest
from importlib import reload
import code
from code.user import User


class BaseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User("1")
        self.expected_list = self.create_transaction()

    def tearDown(self) -> None:
        if os.path.exists("../data/1.pickle"):
            os.remove("../data/1.pickle")

    def create_transaction(self):
        transaction = {}
        for category in self.user.spend_categories:
            transaction[category] = []
        return transaction

    def add_record(self, category, record):

        self.expected_list[category].append(record)



if __name__ == '__main__':
    unittest.main()
