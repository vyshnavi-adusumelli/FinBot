"""
Tests budget command
"""
import time
import unittest
from src import teleBot
from bot_utils import BotTest


class TestBudget(BotTest):
    """
    Test file for budget
    """

    def test_budget_command(self):
        """
        Tests the budget command
        """
        msg = self.create_text_message('/budget')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/budget'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /budget command, there should be a next step"
        # there should not be any exceptions
        # assert self.bot.worker_pool.exception_info is None

        # send the budget amount
        reply = self.create_text_message("120.00")
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == "120.00"
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the reply to budget, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # assert the budget was added to the user
        chat_id = str(reply.chat.id)
        assert chat_id in teleBot.user_list
        user_budget = teleBot.user_list[chat_id].monthly_budget
        assert user_budget == 120.00

    def test_budget_command_invalid(self):
        """
        Tests the budget command for invalid budget
        """
        msg = self.create_text_message('/budget')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/budget'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /budget command, there should be a next step"
        # there should not be any exceptions
        # assert self.bot.worker_pool.exception_info is None

        # send the budget amount
        reply = self.create_text_message("-19.00")
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == "-19.00"
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the reply to budget, there should not be a next step"
        # # there should not be any exceptions
        # assert self.bot.worker_pool.exception_info is None

        # assert the budget was not changed for the user
        chat_id = str(reply.chat.id)
        assert chat_id in teleBot.user_list
        user_budget = teleBot.user_list[chat_id].monthly_budget
        assert user_budget != -19.00
