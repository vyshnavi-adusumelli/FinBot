
from bot_utils import BotTest
import unittest
import time
from src import teleBot


class TestListCustomCategory(BotTest):
    """
        Test file for add custom category
    """
    def test_list_custom_category_command(self):
        """
        Tests the add custom category command
        """

        # creation of mock data
        msg = self.create_text_message('/categoryAdd')
        self.bot.process_new_messages([msg])
        time.sleep(3)
        custom_category = "books"
        reply = self.create_text_message(custom_category)
        self.bot.process_new_messages([reply])
        time.sleep(3)

        # test for validating category list command
        msg = self.create_text_message('/categoryList')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/categoryList'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 0, \
            "For the /categoryList command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # assert the custom category was added to the user
        chat_id = str(msg.chat.id)
        content = teleBot.user_list[chat_id].transactions
        categories = []
        for category in content:
            categories.append(category)
        assert custom_category in categories

if __name__ == '__main__':
    unittest.main()
