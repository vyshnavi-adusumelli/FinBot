"""
Test for the deleteHistory function
"""

import unittest

import code.code
from code.code import deleteHistory


class TestDeleteHistory(unittest.TestCase):
    """
    Unit test for deleteHistory
    """

    def test_delete_history_none(self):
        """
        Given no chat_id, the list should not change
        """
        # given the user_list
        expected_list = code.code.user_list.copy()
        # after deleting with no user
        deleteHistory("")
        assert code.code.user_list == expected_list
        # given adding one user
        expected_list = {"1": ["Test_History"]}
        code.code.user_list = expected_list
        # when no user is passed
        deleteHistory("")
        assert code.code.user_list == expected_list

    def test_delete_valid(self):
        """
        Given there is one user
        deleting a user
        should remove it from the user list
        """
        # given adding one user
        expected_list = {"1": ["Test_History"]}
        code.code.user_list = expected_list
        # when another user is passed
        deleteHistory("2")
        assert "1" in code.code.user_list
        assert code.code.user_list == expected_list

        # When deleting the present user
        deleteHistory("1")
        assert "1" not in code.code.user_list
        assert code.code.user_list == {}

    def test_delete_multiple(self):
        """
        Given there is a chat history
        deleting a user
        should remove it from the user list
        """

        # given adding two user
        expected_list = {"1": ["Test_History"], "2": ["Test_History_2"]}
        code.code.user_list = expected_list
        # when one user is passed
        deleteHistory("1")
        assert "1" not in code.code.user_list
        assert code.code.user_list == {"2": ["Test_History_2"]}
        # when the last user is passed
        deleteHistory("2")
        assert "2" not in code.code.user_list
        assert code.code.user_list == {}

    def test_delete_one_record(self):
        """
        Given there is one user
        deleting one record from the user
        should remove it from the user list
        """
        # given adding one user
        starting_list = {"1": ["Test_History", "Test_History_2"]}
        expected_list = {"1": ["Test_History_2"]}
        code.code.user_list = starting_list
        # when another user is passed
        deleteHistory("1", ["Test_History"])
        assert "1" in code.code.user_list
        assert code.code.user_list == expected_list

    def test_delete_multiple_record(self):
        """
        Given there is one user
        deleting one record from the user
        should remove it from the user list
        """
        # given adding one user
        starting_list = {"1": ["Test_History", "Test_History_2", "Test_History_3"]}
        expected_list = {"1": ["Test_History_3"]}
        code.code.user_list = starting_list
        # when another user is passed
        deleteHistory("1", ["Test_History_2", "Test_History"])
        assert "1" in code.code.user_list
        assert code.code.user_list == expected_list

    def test_delete_all_record(self):
        """
        Given there is one user
        deleting all record from the user
        should remove it from the user list
        """
        # given adding one user
        starting_list = {"1": ["Test_History", "Test_History_2"]}
        code.code.user_list = starting_list
        # when another user is passed
        deleteHistory("1", ["Test_History", "Test_History_2"])
        assert "1" not in code.code.user_list
        assert code.code.user_list == {}