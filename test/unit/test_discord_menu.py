import unittest
from unittest.mock import Mock, patch
from discordBot import menu  # Import your actual bot's code

class TestMenuCommand(unittest.TestCase):
    @patch('your_discord_bot.menu')
    async def test_menu_command(self, mock_menu):
        # Create a mock context (ctx)
        ctx = Mock()

        # Call the menu command
        await menu(ctx)

        # Assert that menu was called
        mock_menu.assert_called_once_with(ctx)

if __name__ == '__main__':
    unittest.main()