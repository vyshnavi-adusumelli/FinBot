"""
Tests edit command
"""
import time
import unittest
from bot_utils import BotTest


class TestEdit(BotTest):
    """
    Test file for edit
    """

    def test_edit_command(self):
        """
        Tests the edit command
        """

        msg = self.create_text_message('/edit')
        self.bot.process_new_messages([msg])
        time.sleep(5)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/edit'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /edit command with no records, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

    def test_edit_command_records(self):
        """
        Tests the edit command with records
        """
        self.create_record(10.00)
        msg = self.create_text_message('/edit')
        self.bot.process_new_messages([msg])
        time.sleep(5)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/edit'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /edit command with records, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # processing a reply
        category = self.user.spend_categories[0]
        date = self.user.transactions[category][0]['Date'].date()
        value = self.user.transactions[category][0]['Value']
        msg_text = f"{date},{category},{value}"
        msg = self.create_text_message(msg_text)
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == msg_text
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /edit command with records, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None



if __name__ == '__main__':
    unittest.main()
