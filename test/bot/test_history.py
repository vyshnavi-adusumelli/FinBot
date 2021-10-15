import time
import unittest
from datetime import datetime
from bot_utils import BotTest, create_text_message, CHAT_ID
import code
from code.code import dateFormat, spend_categories


class TestHistory(BotTest):

    def test_history_command_no_history(self):
        assert len(code.code.user_list) == 0
        msg = create_text_message('/history')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        assert msg.chat.id == CHAT_ID
        assert msg.text == '/history'
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For /history with no history, there should not be a next step"

    def test_history_command_with_history(self):
        # artifically creating history
        lst = [datetime.now().today().strftime(dateFormat), spend_categories[0], 10.0]
        expected_dict = {str(CHAT_ID): lst}
        code.code.user_list = expected_dict
        # querying history
        msg = create_text_message('/history')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        assert msg.chat.id == CHAT_ID
        assert msg.text == '/history'
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0,\
            "For /history with history, there should not be a next step"


if __name__ == '__main__':
    unittest.main()
