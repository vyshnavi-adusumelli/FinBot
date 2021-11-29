"""
Tests delete command
"""
import time
import unittest
from bot_utils import BotTest
from src import bot


class TestDelete(BotTest):
    """
    Test file for delete
    """

    def test_delete_command(self):
        """
        Tests the delete command
        """
        msg = self.create_text_message('/delete')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/delete'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /delete command with no records, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

    def test_delete_command_records(self):
        """
        Tests the delete command with correct formats
        """
        self.create_record(10.00)
        msg = self.create_text_message('/delete')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/delete'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /delete command with records, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the current day
        dateFormat = '%m/%d/%Y'
        tr = self.user.transactions[self.user.spend_categories[0]][0]
        date = tr['Date'].strftime(dateFormat)
        msg = self.create_text_message(date)
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == date
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /delete command with records, there should be a next step"


        # reply YES
        msg = self.create_text_message("YES")
        self.bot.process_new_messages([msg])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == "YES"
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /delete command with records, there should be a next step"

        # assert the record was deleted
        CHAT_ID = str(msg.chat.id)
        assert bot.user_list[CHAT_ID].get_number_of_transactions() == 0





if __name__ == '__main__':
    unittest.main()
