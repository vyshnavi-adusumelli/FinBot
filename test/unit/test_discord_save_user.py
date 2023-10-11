"""
Test for the save_user method
"""
import os
import pathlib
import pickle

from discord_BaseCase import discord_BaseCase


def users_equal(user_1, user_2):
    if user_1.spend_categories != user_2.spend_categories:
        return "Spend Categories do not match"
    if user_1.spend_display_option != user_2.spend_display_option:
        return "spend_display_option do not match"
    if user_1.transactions != user_2.transactions:
        return "transactions do not match"
    if user_1.edit_transactions != user_2.edit_transactions:
        return "edit_transactions do not match"
    if user_1.edit_category != user_2.edit_category:
        return "edit_category do not match"
    if user_1.monthly_budget != user_2.monthly_budget:
        return "monthly_budget do not match"
    return True


class TestSaveUser(discord_BaseCase):
    """
    Unit test for save_user
    """

    def test_save_no_history(self):
        """
        given a valid user, saving and loading should return the same user
        """
        prev_user = self.user
        # with no history, call save_user
        self.user.save_user(2)
        # assert the pickle exists
        abspath = pathlib.Path("discordData/2.pickle").absolute()
        assert os.path.exists(abspath)

        with open(abspath, "rb") as f:
            new_user = pickle.load(f)
        # assert they are equal
        assert new_user is not None
        are_equal = users_equal(prev_user, new_user)
        if not are_equal:
            assert False, are_equal

    def test_valid_history(self):
        """
        given a valid user, saving should yield the same user
        """
        self.user.spend_categories.append("TEST")
        self.user.spend_display_option.append("otherTest")
        self.user.transactions[self.user.spend_categories[0]].append({"TEST": 0})
        self.user.edit_transactions["TEST"] = 0
        self.user.edit_category["TEST"] = 2
        self.user.monthly_budget = 100
        prev_user = self.user
        # with history, call save_user
        self.user.save_user(2)
        # assert the pickle exists
        abspath = pathlib.Path("discordData/2.pickle").absolute()
        assert os.path.exists(abspath)
        with open(abspath, "rb") as f:
            new_user = pickle.load(f)
        # assert they are equal
        assert new_user is not None
        are_equal = users_equal(prev_user, new_user)
        if not are_equal:
            assert False, are_equal
