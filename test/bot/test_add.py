"""
Tests add command
"""
import time
import unittest
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
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /add command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None




if __name__ == '__main__':
    unittest.main()
