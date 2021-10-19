"""
Tests the get_user_history method
"""
import unittest

import code.code
from code.code import getUserHistory


class TestGetUserHistory(unittest.TestCase):
    """
    Unit test for get user history
    """

    def setUp(self) -> None:
        # reset the user list
        code.code.user_list = {}

    def test_get_user_history_none(self):
        """
        Given there are no users, attempting to get a user
        should return None
        """
        assert not code.code.user_list

        # asserting getting the user history returns non
        assert getUserHistory(0) is None
        assert getUserHistory(1) is None
        assert getUserHistory(2) is None

    def test_get_user_history_invalid(self):
        """
        Given there are user histories,
        getting the user history of a non-present user
        should return None
        """
        # assert code.code.user_list is  {}
        code.code.user_list["1"] = ["TestRecordOne"]

        assert getUserHistory(0) is None
        assert getUserHistory(2) is None
        code.code.user_list = {}

    def test_get_user_history_valid(self):
        """
        Given there is user history,
        getting the user history of a present user
        should return the history
        """
        assert len(code.code.user_list) == 0
        code.code.user_list["1"] = ["TestRecordOne"]
        # getting the user
        assert getUserHistory(1) == ["TestRecordOne"]
        # adding another user
        code.code.user_list["2"] = ["TestRecordTwo"]
        # getting the user
        assert getUserHistory(2) == ["TestRecordTwo"]
        # appending to user 1
        code.code.user_list["1"].append("TestRecordThree")
        assert getUserHistory(1) == ["TestRecordOne", "TestRecordThree"]
        assert getUserHistory(2) == ["TestRecordTwo"]
