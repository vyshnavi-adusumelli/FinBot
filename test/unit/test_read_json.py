"""
Test for the read_json method
"""
import io
import os
import unittest.mock
from shutil import copyfile

import code.code
from code.code import read_json


class TestReadJson(unittest.TestCase):
    """
    Unit test for read_json
    """

    def setUp(self) -> None:
        """
        if the expense record exists, move it
        """
        if os.path.exists('expense_record.json'):
            os.replace("expense_record.json", "test.json")


    def tearDown(self) -> None:
        """
        if the expense record was moved, restore it
        """
        # if we moved over files due to tests, remove it
        if os.path.exists('expense_record.json'):
            os.remove("expense_record.json")
        if os.path.exists('test.json'):
            os.replace("test.json", "expense_record.json")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_no_file(self, mock_stdout):
        """
        Given no file, a error should be printed
        :param mock_stdout: stdout
        """
        assert not os.path.exists("expense_record.json")
        # calling read_json should print an error to console
        expected_output = "---------NO RECORDS FOUND---------\n"
        read_json()
        self.assertEqual(expected_output, mock_stdout.getvalue())

    def test_valid_file_1(self):
        """
        given a valid file test_1.json, user_list should be the same
        """
        expected_1 = {"1": ["Test1"]}
        # move the test_1.json to expected_list.json
        assert not os.path.exists("expense_record.json")
        copyfile("data/test_1.json", "expense_record.json")

        # call the read_json
        read_json()
        assert code.code.user_list == expected_1

    def test_valid_file_2(self):
        """
        given a valid file test_2.json, user_list should be the same
        """

        expected_2 = {"1": ["Test1", "Test2"]}
        # move the test_1.json to expected_list.json
        assert not os.path.exists("expense_record.json")
        copyfile("data/test_2.json", "expense_record.json")

        # call the read_json
        read_json()
        assert code.code.user_list == expected_2

    def test_valid_file_3(self):
        """
        given a valid file test_3.json, user_list should be the same
        """
        expected_3 = {"1": ["Test1", "Test2"], "2": ["Test3"]}

        # move the test_1.json to expected_list.json
        assert not os.path.exists("expense_record.json")
        copyfile("data/test_3.json", "expense_record.json")

        # call the read_json
        read_json()
        assert code.code.user_list == expected_3
