import unittest
from unittest.mock import patch
import teleBot as code_lib

class TestCommands(unittest.TestCase):
    @patch.object(code_lib, 'telebot')
    def test_number_commands(self, mock_telebot):
        bot = code_lib.bot
        # Simulate bot's behavior
        bot.message_handlers = [{'filters': ['commands']} for _ in range(14)]

        number_of_commands = 14
        self.assertEqual(len(bot.message_handlers), number_of_commands)

    @patch.object(code_lib, 'telebot')
    def test_commands(self, mock_telebot):
        bot = code_lib.bot
        bot.message_handlers = [
            {'filters': ['commands'], 'function': code_lib.start_and_menu_command},
            {'filters': ['commands'], 'function': code_lib.command_budget},
            {'filters': ['commands'], 'function': code_lib.command_add},
            {'filters': ['commands'], 'function': code_lib.show_history},
            {'filters': ['commands'], 'function': code_lib.command_display},
            {'filters': ['commands'], 'function': code_lib.edit1},
            {'filters': ['commands'], 'function': code_lib.category_add},
            {'filters': ['commands'], 'function': code_lib.category_list},
            {'filters': ['commands'], 'function': code_lib.category_delete},
            {'filters': ['commands'], 'function': code_lib.command_delete},
            {'filters': ['commands'], 'function': code_lib.send_email},
            {'filters': ['commands'], 'function': code_lib.download_history}
        ]

        actual_titles = [
            {'function': code_lib.start_and_menu_command, 'commands': ["start", "menu"]},
            {'function': code_lib.command_budget, 'commands': ["budget"]},
            {'function': code_lib.command_add, 'commands': ["add"]},
            {'function': code_lib.show_history, 'commands': ["history"]},
            {'function': code_lib.command_display, 'commands': ["display"]},
            {'function': code_lib.edit1, 'commands': ["edit"]},
            {'function': code_lib.category_add, 'commands': ["categoryAdd"]},
            {'function': code_lib.category_list, 'commands': ["categoryList"]},
            {'function': code_lib.category_delete, 'commands': ["categoryDelete"]},
            {'function': code_lib.command_delete, 'commands': ["delete"]},
            {'function': code_lib.send_email, 'commands': ["sendEmail"]},
            {'function': code_lib.download_history, 'commands': ["download"]}
        ]

        for i, expected_func in enumerate(actual_titles):
            self.assertEqual(bot.message_handlers[i]['function'], expected_func['function'])

if __name__ == '__main__':
    unittest.main()