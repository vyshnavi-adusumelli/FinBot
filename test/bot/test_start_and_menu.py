"""
Tests start and menu commands
"""
import time
import unittest
from bot_utils import BotTest


class TestStartMenu(BotTest):
    """
    Test file for start and menu comands
    """

    def test_start_command(self):
        """
        Tests the start command
        """
        msg = BotTest.create_text_message('/start')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/start'
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /start command, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

    def test_menu_command(self):
        """
        Tests the menu command
        """
        msg = BotTest.create_text_message('/menu')
        self.bot.process_new_messages([msg])
        time.sleep(3)
        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/menu'
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /menu command, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None


if __name__ == '__main__':
    unittest.main()
