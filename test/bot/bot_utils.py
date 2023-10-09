"""
Util functions for bot tests
"""
import logging
import os
import pathlib
import unittest
from datetime import datetime
from importlib import reload

from telebot import types
import sys
# sys.path.append("E:\SE\project phase 3\slashbot\src")
import src.teleBot
from src.teleUser import User

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
        abspath = pathlib.Path("teleData").absolute()
        if not os.path.exists(abspath):
            os.mkdir(abspath)
        reload(src.teleBot)
        src.teleBot.api_token = os.environ['API_TOKEN']
        self.bot = src.teleBot.bot
        self.user = User(str(CHAT_ID))
        self.user.save_user(str(CHAT_ID))
        self.chat_id = CHAT_ID
        # reloads the user list
        src.teleBot.user_list = src.teleBot.get_users()
        # asserts the current user has no data
        assert self.user.get_number_of_transactions() == 0

    def tearDown(self) -> None:
        # Clearing out next step handlers
        self.bot.next_step_backend.handlers = {}
        path = f"teleData/{CHAT_ID}.pickle"
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
        src.teleBot.user_list = src.teleBot.get_users()
        assert CHAT_ID in src.teleBot.user_list.keys()

    def create_text_message(self, text: str) -> types.Message:
        """
        Creates a text message
        :param text: text of the message
        :return: The created message to be sent
        """
        params = {'text': text}
        chat = types.User(int(CHAT_ID), False, 'test')
        return types.Message(1, None, None, chat, 'text', params, "")

    def create_callback_query(self, data: str, message: types.Message) -> types.CallbackQuery:
        """
        Creates a text message
        :param text: text of the message
        :return: The created message to be sent
        """
        chat = types.User(int(CHAT_ID), False, 'test')
        return types.CallbackQuery(1, CHAT_ID, data, chat, message)
