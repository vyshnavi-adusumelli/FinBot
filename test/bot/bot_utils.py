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
        """
        Creates a new user and ensures no data was left over
        :return: None
        """
        os.chdir("test/bot")
        reload(code.bot)
        self.bot = code.bot.bot
        self.user = User(str(CHAT_ID))
        # reloads the user list
        # src.bot.user_list = src.bot.get_users()
        # asserts the current user has no data
        assert self.user.get_number_of_transactions() == 0

    def tearDown(self) -> None:
        # Clearing out next step handlers
        self.bot.next_step_backend.handlers = {}
        path = f"../data/{CHAT_ID}.pickle"
        if os.path.isfile(path):
            os.remove(path)
        # verifying all old info was deleted
        self.user = User(CHAT_ID)
        assert self.user.get_number_of_transactions() == 0
        os.chdir("../..")

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
        chat = types.User(CHAT_ID, False, 'test')
        return types.Message(1, None, None, chat, 'text', params, "")
