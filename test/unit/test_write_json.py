"""
Test for the write_json method
"""
import io
import json
import os
import unittest.mock
# import src.code
# from src.code import write_json


class TestWriteJson(unittest.TestCase):
    """
    Unit test for write_json
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
        Given no file, there should be no error
        :param mock_stdout: stdout
        """
        assert not os.path.exists("expense_record.json")
        # calling write_json should not print an error to console
        expected_output = ""
        write_json(src.code.user_list)
        self.assertEqual(expected_output, mock_stdout.getvalue())

    def test_valid_file_1(self):
        """
        given a valid user_list, the file should match
        test_1.json
        """
        expected_1 = {"1": ["Test1"]}

        # call the write_json
        write_json(expected_1)
        # assert the expense_record.json exists
        assert os.path.exists('expense_record.json')

        # assert the test file exists
        assert os.path.exists('test/data/test_1.json')

        # load in the expense_record.json
        actual = None
        try:
            with open('expense_record.json') as expense_record:
                actual = json.load(expense_record)
        except ValueError:
            assert False, "Error loading expense_record.json"
        # assert they are equal
        assert actual == expected_1

    def test_valid_file_2(self):
        """
        given a valid user_list, the file should match
        test_2.json
        """
        expected_2 = {"1": ["Test1", "Test2"]}

        # call the write_json
        write_json(expected_2)
        # assert the expense_record.json exists
        assert os.path.exists('expense_record.json')

        # assert the test file exists
        assert os.path.exists('test/data/test_2.json')

        # load in the expense_record.json
        actual = None
        try:
            with open('expense_record.json') as expense_record:
                actual = json.load(expense_record)
        except ValueError:
            assert False, "Error loading expense_record.json"
        # assert they are equal
        assert actual == expected_2

    def test_valid_file_3(self):
        """
        given a valid user_list, the file should match
        test_1.json
        """
        expected_3 = {"1": ["Test1", "Test2"], "2": ["Test3"]}

        # call the write_json
        write_json(expected_3)
        # assert the expense_record.json exists
        assert os.path.exists('expense_record.json')

        # assert the test file exists
        assert os.path.exists('test/data/test_3.json')

        # load in the expense_record.json
        actual = None
        try:
            with open('expense_record.json') as expense_record:
                actual = json.load(expense_record)
        except ValueError:
            assert False, "Error loading expense_record.json"
        # assert they are equal
        assert actual == expected_3
