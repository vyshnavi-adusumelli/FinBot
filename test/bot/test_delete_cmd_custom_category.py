
from bot_utils import BotTest
import unittest
import time
from src import teleBot


class TestDeleteCustomCategory(BotTest):
    """
        Test file for deleting custom category
    """
    def test_delete_custom_category_command(self):
        """
        Tests the delete custom category command
        """

        # creation of mock data
        msg = self.create_text_message('/categoryAdd')
        self.bot.process_new_messages([msg])
        time.sleep(3)
        custom_category = "books"
        reply = self.create_text_message(custom_category)
        self.bot.process_new_messages([reply])
        time.sleep(3)

        # test case for validating category delete command
        msg = self.create_text_message('/categoryDelete')
        self.bot.process_new_messages([msg])
        time.sleep(3)

        # assert the message was sent, and text was not changed
        assert msg.chat.id is not None
        assert msg.text == '/categoryDelete'
        # there should be a next step handler
        assert len(self.bot.next_step_backend.handlers) == 1, \
            "For the /categoryDelete command, there should be a next step"
        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None

        # send the custom category
        reply = self.create_text_message(custom_category)
        self.bot.process_new_messages([reply])
        time.sleep(3)

        #delete the newly created custom category
        chat_id = str(reply.chat.id)
        content = teleBot.user_list[chat_id].transactions
        categories = []
        for category in content:
            categories.append(category)
        assert custom_category not in categories

if __name__ == '__main__':
    unittest.main()
