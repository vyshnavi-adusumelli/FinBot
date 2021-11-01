"""
Tests history command
"""
import time
import unittest
from bot_utils import BotTest


class TestHistory(BotTest):
    """
    Test file for history
    """

    def test_history_command(self):
        """
        Tests the history command
        """
        msg = self.create_text_message('/history')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/history'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /history command, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

    def test_history_command_records(self):
        """
        Tests the history command
        """
        self.create_record(10.00)
        msg = self.create_text_message('/history')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/history'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /history command, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None




if __name__ == '__main__':
    unittest.main()
