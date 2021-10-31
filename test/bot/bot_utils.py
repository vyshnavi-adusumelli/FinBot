"""
Util functions for bot tests
"""

import os
import pathlib
import unittest
from datetime import datetime
from importlib import reload

from telebot import types

import code.bot
from code.user import User

CHAT_ID = os.environ['CHAT_ID'] if 'CHAT_ID' in os.environ else 1
TOKEN = os.environ['API_TOKEN'] if 'API_TOKEN' in os.environ else 0


class BotTest(unittest.TestCase):
    """
    Base test class for Bot Tests
    """

    def setUp(self) -> None:
        """
        Creates a new user and ensures no data was left over
        :return: None
        """
        abspath = pathlib.Path("../data").absolute()
        if not os.path.exists(abspath):
            os.mkdir(abspath)
        reload(code.bot)
        code.bot.api_token = os.environ['API_TOKEN']
        self.bot = code.bot.bot
        self.user = User(str(CHAT_ID))
        self.user.save_user(str(CHAT_ID))
        # reloads the user list
        code.bot.user_list = code.bot.get_users()
        # asserts the current user has no data
        assert self.user.get_number_of_transactions() == 0

    def tearDown(self) -> None:
        # Clearing out next step handlers
        self.bot.next_step_backend.handlers = {}
        path = f"../data/{CHAT_ID}.pickle"
        abspath = pathlib.Path(path).absolute()
        if os.path.exists(abspath):
            os.remove(path)
        # verifying all old info was deleted
        self.user = User(CHAT_ID)
        assert self.user.get_number_of_transactions() == 0

    def create_record(self, amount: float) -> None:
        """
        Creates a record in the user list for the given amount
        :param amount: amount to add
        :return: None
        """
        self.user.add_transaction(datetime.now(), self.user.spend_categories[0], amount, CHAT_ID)
        self.user.save_user(CHAT_ID)
        code.bot.user_list = code.bot.get_users()
        assert CHAT_ID in code.bot.user_list.keys()

    def create_text_message(self, text: str) -> types.Message:
        """
        Creates a text message
        :param text: text of the message
        :return: The created message to be sent
        """
        params = {'text': text}
        chat = types.User(int(CHAT_ID), False, 'test')
        return types.Message(1, None, None, chat, 'text', params, "")
