"""
Test for the deleteHistory function
"""

from datetime import datetime
from BaseCase import BaseCase


class TestValidateDateFormat(BaseCase):
    """
    Unit test for validate_date_format
    """

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

