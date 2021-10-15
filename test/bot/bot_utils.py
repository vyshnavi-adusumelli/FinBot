import os
import unittest

from telebot import types
import code

CHAT_ID = os.environ['CHAT_ID'] if 'CHAT_ID' in os.environ else 1
TOKEN = os.environ['TOKEN'] if 'TOKEN' in os.environ else 0


def create_text_message(text):
    params = {'text': text}
    chat = types.User(CHAT_ID, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


class BotTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bot = code.code.bot

    def tearDown(self) -> None:
        self.bot.process_new_messages([create_text_message("clear_text")])
