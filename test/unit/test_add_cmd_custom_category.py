import unittest
from unittest.mock import Mock, patch
import teleBot

class TestAddCustomCategory(unittest.TestCase):
    def test_add_custom_category_command(self):
        # Mock the necessary dependencies
        with patch.object(teleBot.bot, 'process_new_messages') as mock_process_messages:
            with patch.object(teleBot.bot, 'next_step_backend', Mock()) as mock_next_step_backend:
                msg = Mock()
                msg.chat.id = "12345"
                msg.text = "/categoryAdd"
                custom_category = "travel"

                # Simulate bot's behavior
                teleBot.bot.process_new_messages.return_value = [msg]
                teleBot.bot.next_step_backend.handlers = []

                # Trigger the command
                teleBot.bot.process_new_messages([msg])

                # Add the custom category
                reply = Mock()
                reply.chat.id = "12345"
                reply.text = custom_category
                teleBot.bot.process_new_messages([reply])

                # Add your assertions here
                # Assert that the custom category was added to the user, possibly by checking bot.user_list

if __name__ == '__main__':
    unittest.main()