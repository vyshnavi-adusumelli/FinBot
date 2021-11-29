"""
Tests add command
"""
import time
import unittest
import sys
sys.path.append("E:\SE\project phase 3\slashbot")
print(sys.path)
from src import bot
from bot_utils import BotTest


class TestAdd(BotTest):
    """
    Test file for add
    """

    def test_add_command(self):
        """
        Tests the add command
        """
        msg = self.create_text_message('/add')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/add'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /add command, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the calendar date
        query = self.create_callback_query("2021,11,01", msg)
        self.bot.process_new_callback_query([query])
        time.sleep(3)

        # assert the query was sent
        assert query.chat_instance.id is not None
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /add command after date, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the category we use
        reply = self.create_text_message(self.user.spend_categories[0])
        category = self.user.spend_categories[0]
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == self.user.spend_categories[0]
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the reply to add, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the amount
        reply = self.create_text_message("1.00")
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == "1.00"
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the reply to add, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # assert the record was added to the user
        chat_id = str(reply.chat.id)
        assert chat_id in bot.user_list
        assert category in bot.user_list[chat_id].transactions
        user_transac = bot.user_list[chat_id].transactions
        assert user_transac[category] != []
        assert user_transac[category][0]['Value'] == 1.0

        # there should be any records added
        assert bot.user_list[str(msg.chat.id)].get_number_of_transactions() == 1


    def test_add_wrong_date(self):
        """
        Tests the add command with an invalid value
        """
        msg = self.create_text_message('/add')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/add'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /add command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the calendar date
        query = self.create_callback_query("prev", msg)
        self.bot.process_new_callback_query([query])
        time.sleep(3)

        # assert the query was sent
        assert query.chat_instance.id is not None
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /add command after date, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the calendar date
        query = self.create_callback_query("", msg)
        self.bot.process_new_callback_query([query])
        time.sleep(3)

        # assert the query was sent
        assert query.chat_instance.id is not None
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /add command after date, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # there should not be any records added
        assert bot.user_list[str(msg.chat.id)].get_number_of_transactions() == 0

    def test_add_wrong_cat(self):
        """
        Tests the add command with an invalid category
        """
        msg = self.create_text_message('/add')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/add'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /add command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the calendar date
        query = self.create_callback_query("2021,11,01", msg)
        self.bot.process_new_callback_query([query])
        time.sleep(3)

        # assert the query was sent
        assert query.chat_instance.id is not None
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /add command after date, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the category we use
        reply = self.create_text_message("INVALID")
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == "INVALID"
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the reply to add with wrong cat, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # there should not be any records added
        assert bot.user_list[str(msg.chat.id)].get_number_of_transactions() == 0


    def test_add_wrong_num(self):
        """
        Tests the add command with an invalid value
        """
        msg = self.create_text_message('/add')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/add'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /add command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the calendar date
        query = self.create_callback_query("2021,11,01", msg)
        self.bot.process_new_callback_query([query])
        time.sleep(3)

        # assert the query was sent
        assert query.chat_instance.id is not None
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /add command after date, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the category we use
        reply = self.create_text_message(self.user.spend_categories[0])
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == self.user.spend_categories[0]
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the reply to add, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the amount we use
        reply = self.create_text_message("-1")
        self.bot.process_new_messages([reply])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert reply.chat.id is not None
        assert reply.text == "-1"
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the reply to add, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # there should not be any records added
        assert bot.user_list[str(msg.chat.id)].get_number_of_transactions() == 0

if __name__ == '__main__':
    unittest.main()
