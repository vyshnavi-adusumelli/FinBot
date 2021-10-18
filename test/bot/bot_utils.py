"""
Util functions for bot tests
"""

import json
import os
import unittest
from datetime import datetime
from importlib import reload
import code
from code.code import dateFormat, spend_categories

from telebot import types


CHAT_ID = os.environ['CHAT_ID'] if 'CHAT_ID' in os.environ else 1
TOKEN = os.environ['TOKEN'] if 'TOKEN' in os.environ else 0


class BotTest(unittest.TestCase):
    """
    Base test class for Bot Tests
    """

    def setUp(self) -> None:
        reload(code.code)
        self.bot = code.code.bot
        if os.path.exists('expense_record.json'):
            os.replace("expense_record.json", "test.json")

    def tearDown(self) -> None:
        # if we moved over files due to tests, remove it
        if os.path.exists('expense_record.json'):
            os.remove("expense_record.json")
        if os.path.exists('test.json'):
            os.replace("test.json", "expense_record.json")

    @staticmethod
    def create_record(amount: float) -> None:
        """
        Creates a record in the user list for the given amount
        :param amount: amount to add
        :return: None
        """
        lst = [datetime.now().today().strftime(dateFormat), spend_categories[0], amount]
        expected_dict = {str(CHAT_ID): lst}
        with open('expense_record.json', 'w', encoding='utf-8') as json_file:
            json.dump(expected_dict, json_file, ensure_ascii=False, indent=4)

    @staticmethod
    def create_text_message(text: str) -> types.Message:
        """
        Creates a text message
        :param text: text of the message
        :return: The created message to be sent
        """
        params = {'text': text}
        chat = types.User(CHAT_ID, False, 'test')
        return types.Message(1, None, None, chat, 'text', params, "")
