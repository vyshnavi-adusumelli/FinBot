"""
Util functions for bot tests
"""

import json
import os
import sys
sys.path.append("../../..")
import unittest
from datetime import datetime
from importlib import reload
import code.bot
from code.user import User
from code.bot import bot

from telebot import types


CHAT_ID = os.environ['CHAT_ID'] if 'CHAT_ID' in os.environ else 1
TOKEN = os.environ['API_TOKEN'] if 'API_TOKEN' in os.environ else 0


class BotTest(unittest.TestCase):
    """
    Base test class for Bot Tests
    """

    def setUp(self) -> None:
        reload(code.bot)
        self.bot = code.bot.bot

    def tearDown(self) -> None:
        pass
        # self.bot.send_message(CHAT_ID, "TEST")

    @staticmethod
    def create_record(amount: float) -> None:
        """
        Creates a record in the user list for the given amount
        :param amount: amount to add
        :return: None
        """
        user = User(CHAT_ID)
        user.add_transaction(datetime.now(), user.spend_categories[0], amount, CHAT_ID)
        user.save_user(CHAT_ID)
        code.bot.user_list = code.bot.get_users()
        assert CHAT_ID in code.bot.user_list.keys()



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
