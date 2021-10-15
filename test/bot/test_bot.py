from bot_utils import BotTest
from code.code import command_delete, command_add, show_history, edit1, command_display, start_and_menu_command


class TestCommands(BotTest):

    def test_commands(self):
        cmds = self.bot.message_handlers
        actual_titles = [{'function': start_and_menu_command, 'commands': ["start", "menu"]},
                         {'function': command_add, 'commands': ["add"]},
                         {'function': show_history, 'commands': ["history"]},
                         {'function': edit1, 'commands': ["edit"]},
                         {'function': command_display, 'commands': ["display"]},
                         {'function': command_delete, 'commands': ["delete"]}]
        assert len(cmds) == len(actual_titles)
        for actual_func, expected_func in zip(cmds, actual_titles):
            assert actual_func['filters']['commands'] == expected_func['commands']
            assert actual_func['function'] == expected_func['function']
