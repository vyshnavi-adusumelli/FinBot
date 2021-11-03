"""
Tests chart command
"""

import time
import unittest
from bot_utils import BotTest

class TestChart(BotTest):
    """
    Test file for chart
    """
    def test_chart_command(self):
        """
        Tests the chart command
        """
        msg = self.create_text_message('/chart')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/chart'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /chart command, there should not be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None