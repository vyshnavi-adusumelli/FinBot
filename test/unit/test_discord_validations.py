#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests the validate_entered_amount method
"""
from discord_BaseCase import discord_BaseCase
from datetime import datetime


class TestValidateEnteredAmount(discord_BaseCase):
    """
    Unit test for get user history
    """

    def test_validate_entered_amount_empty(self):
        """
        Asserts when validate_entered_amount is given an empty string,
        0 is returned

        """
        # given an empty string for amount entered, 0 should be returned
        assert self.user.validate_entered_amount("") == 0

    def test_validate_entered_amount_string(self):
        """
        Asserts when validate_entered_amount is given a string
        0 is returned
        """
        # given an string, 0 should be returned
        assert self.user.validate_entered_amount("Test") == 0
        # given a string that contains numbers and a string
        assert self.user.validate_entered_amount("000t") == 0

    def test_validate_entered_amount_nan(self):
        """
        Asserts when validate_entered_amount is given an invalid
        number, 0 is returned
        """
        # given a negative number
        assert self.user.validate_entered_amount("-1") == 0
        # given 0
        assert self.user.validate_entered_amount("0") == 0
        # given a number with dollar sign
        assert self.user.validate_entered_amount("$10") == 0
        # given a number with 2 decimals
        assert self.user.validate_entered_amount("10..0") == 0

    def test_validate_entered_amount_valid(self):
        """
        Asserts when validate_entered_amount is given an valid
        number, the number is returned
        """
        # given a positive number
        assert self.user.validate_entered_amount("1") == 1.00
        # given a positive number with decimals
        assert self.user.validate_entered_amount("10.10") == 10.10
        # given a number with 14 digits
        assert self.user.validate_entered_amount("1000000000.00") == 1000000000.00

    def test_valid_date(self):
        """
        Given no transactions, the list should not change
        """
        date = datetime.today()
        # format it as a year
        dateFormat = '%d-%b-%Y'
        monthFormat = '%b-%Y'
        validated_d_m_y = self.user.validate_date_format(date.strftime(dateFormat), dateFormat)
        assert validated_d_m_y.month == date.month
        assert validated_d_m_y.day == date.day
        assert validated_d_m_y.year == date.year
        validated_m_y = self.user.validate_date_format(date.strftime(monthFormat), monthFormat)
        assert validated_m_y.month == date.month
        assert validated_m_y.year == date.year

    def test_invalid(self):
        """
        Given there is one user
        deleting a transaction
        should remove it
        """
        date = datetime.today()
        # invalid formats
        dateFormat = 'random'
        error = self.user.validate_date_format(date.strftime('%d-%b-%Y'), dateFormat)
        assert error is None
        # mismatched formats
        dateFormat = '%d-%b-%Y'
        monthFormat = '%b-%Y'
        validated_m_y = self.user.validate_date_format(date.strftime(dateFormat), monthFormat)
        assert validated_m_y is None

