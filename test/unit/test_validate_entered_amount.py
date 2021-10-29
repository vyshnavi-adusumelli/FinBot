#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests the validate_entered_amount method
"""
from BaseCase import BaseCase


class TestValidateEnteredAmount(BaseCase):
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
        assert self.user.validate_entered_amount("1") == "1.00"
        # given a positive number with decimals
        assert self.user.validate_entered_amount("10.10") == "10.10"
        # given a number with 14 digits
        assert self.user.validate_entered_amount("1000000000.00") == "1000000000.00"
