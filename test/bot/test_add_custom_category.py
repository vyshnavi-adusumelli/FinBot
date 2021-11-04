
from bot_utils import BotTest
import unittest
import time
from code import bot


class TestAddCustomCategory(BotTest):
    """
        Test file for add custom category
    """
    def test_add_custom_category_command(self):
        """
        Tests the add custom category command
        """
        msg = self.create_text_message('/categoryAdd')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/categoryAdd'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /categoryAdd command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

if __name__ == '__main__':
    unittest.main()
