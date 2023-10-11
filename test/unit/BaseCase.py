import os.path
import pathlib
import unittest

try:
    from src import teleUser
    import src.teleUser as teleUser
    from src.teleUser import User
except:
    from teleUser import User

class BaseCase(unittest.TestCase):
    """
    Base case class for all other unit tests to inherit from
    """
    def setUp(self) -> None:
        """
        Creates a new user
        """
        # os.chdir("test")
        abspath = pathlib.Path("teleData").absolute()
        if not os.path.exists(abspath):
            os.mkdir(abspath)

        print(os.getcwd())
        self.user = User("1")
        self.expected_list = self.create_transaction()

    def tearDown(self) -> None:
        """
        Removes the user pickle
        """
        abspath = pathlib.Path("teleData").absolute()
        if not os.path.exists(abspath):
            os.mkdir(abspath)

    def create_transaction(self):
        """
        Creates the dictionary of transactions
        """
        transaction = {}
        for category in self.user.spend_categories:
            transaction[category] = []
        return transaction

    def add_record(self, category, record):
        """
        Adds a record to the internal expected transactions
        """
        self.expected_list[category].append(record)


if __name__ == '__main__':
    unittest.main()
