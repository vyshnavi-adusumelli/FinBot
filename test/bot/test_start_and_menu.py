import time
import unittest
from bot_utils import BotTest, create_text_message


class TestStartMenu(BotTest):

    def test_start_command(self):
        msg = create_text_message('/start')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        assert msg.chat.id is not None
        assert msg.text == '/start'
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /start command, there should not be a next step"

    def test_menu_command(self):
        msg = create_text_message('/menu')
        self.bot.process_new_messages([msg])
        time.sleep(3)
        assert msg.chat.id is not None
        assert msg.text == '/menu'
        # there should not be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /menu command, there should not be a next step"


if __name__ == '__main__':
    unittest.main()
