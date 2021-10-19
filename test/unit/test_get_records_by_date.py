"""
Test for the getRecordsByDate function
"""

import unittest
from datetime import datetime
import code.code
from code.code import get_records_by_date


class TestGetRecordsByDate(unittest.TestCase):
    """
    Unit test for deleteHistory
    def get_records_by_date(date, chat_id, is_month):

    By this method, tests have been completed that the user is present
    Thus, there are no tests for user not present
    """
    # given the user_list
    expected_list = None

    def setUp(self) -> None:
        self.expected_list = ["15-Oct-2021 11:56,Transport,1.0",
                              "1-Oct-2021 11:56,Test2,1.0",
                              "18-Oct-2021 11:56,Test3,1.0"]

    def test_user_date_not_present(self):
        """
        Given there is one user
        calling get_records_by_date with a non-present date
        should return []
        """
        wrong_date = datetime.now()
        # make the date year 1, month 1, day 1
        wrong_date = wrong_date.replace(1, 1, 1)
        # given the user_list
        today_date = datetime.now().strftime("%d-%b-%Y %H:%M")
        expected_list = [f'{today_date},Transport,1.0']
        code.code.user_list = {"1": expected_list}

        user_history = get_records_by_date(wrong_date, 1, False)
        # there should be no records
        assert user_history == []
        user_history = get_records_by_date(wrong_date, 1, True)
        # there should be no records
        assert user_history == []

    def test_get_by_month(self):
        """
        Given there is one user
        calling get_records_by_date by month
        """
        code.code.user_list = {"1": self.expected_list}

        october = datetime.now()
        # make the date match october 2021
        october = october.replace(year=2021, month=10).date()
        user_history = get_records_by_date(october, 1, True)
        # there should be no records
        assert user_history == self.expected_list

    def test_get_by_day(self):
        """
        Given there is one user
        calling get_records_by_date with a valid date
        """
        code.code.user_list = {"1": self.expected_list}

        october = datetime.now()
        # make the date match october 2021
        october = october.replace(year=2021, month=10).date()
        user_history = get_records_by_date(october, 1, True)
        # there should be october records
        assert user_history == self.expected_list
        # add another record but in a different month
        self.expected_list.append("18-Nov-2021 11:56,Test3,1.0")
        user_history = get_records_by_date(october, 1, True)
        code.code.user_list["1"] = self.expected_list
        self.expected_list.remove("18-Nov-2021 11:56,Test3,1.0")
        assert user_history == self.expected_list

    def test_get_by_all(self):
        """
        Given there is one user
        calling all
        """
        # given the user_list
        self.expected_list = ["15-Oct-2021 11:56,Transport,1.0",
                              "1-Oct-2021 11:56,Test2,1.0",
                              "18-Oct-2021 11:56,Test3,1.0"]
        code.code.user_list = {"1": self.expected_list}

        user_history = get_records_by_date("all", 1, True)
        # there should all
        assert user_history == self.expected_list
        # add another record but in a different month
        self.expected_list.append("18-Nov-2021 11:56,Test3,1.0")
        user_history = get_records_by_date("all", 1, True)
        code.code.user_list["1"] = self.expected_list
        assert user_history == self.expected_list
