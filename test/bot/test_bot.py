"""
Unit test to check all commands are present
"""
import code.code as code_lib
from bot_utils import BotTest


class TestCommands(BotTest):
    """
    Test class to test commands and functions
    """

    def test_number_commands(self) -> None:
        """
        Tests that the correct number of commands are present
        :return:
        """
        bot_commands = self.bot.message_handlers
        number_of_commands = 6
        # assert there is the right number of commands
        assert len(bot_commands) == number_of_commands

    def test_commands(self) -> None:
        """
        Tests if commands are present, and if they are hooked
        to the correct function
        :return: None
        """
        bot_commands = self.bot.message_handlers
        # dictionary of functions and commands to trigger the function
        actual_titles = [{'function': code_lib.start_and_menu_command,
                          'commands': ["start", "menu"]},
                         {'function': code_lib.command_add, 'commands': ["add"]},
                         {'function': code_lib.show_history, 'commands': ["history"]},
                         {'function': code_lib.edit1, 'commands': ["edit"]},
                         {'function': code_lib.command_display, 'commands': ["display"]},
                         {'function': code_lib.command_delete, 'commands': ["delete"]}]
        # assert each function and command matches
        for actual_func, expected_func in zip(bot_commands, actual_titles):
            assert actual_func['filters']['commands'] == expected_func['commands']
            assert actual_func['function'] == expected_func['function']

        # there should not be any exceptions
        assert self.bot.worker_pool.exception_info is None
