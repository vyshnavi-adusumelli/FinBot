"""
Tests the add_monthly_budget_method
"""

from BaseCase import BaseCase


class TestAddMonthlyBudget(BaseCase):
    """
    Unit test for add monthly budget
    """
    def add_monthly_budget_valid(self):
        """
        Asserts when add_monthly_budget is given a float value

        """
        assert self.user.monthly_budget == 0
        amount = 10.00
        self.user.add_monthly_budget(amount, 1)
        assert self.user.monthly_budget == amount

    def add_monthly_budget_invalid(self):
        """
        Asserts when add_monthly_budget is given 0

        """
        assert self.user.monthly_budget == 0
        amount_valid = 10.00
        self.user.add_monthly_budget(amount_valid, 1)
        assert self.user.monthly_budget == amount
        amount = 0.00
        self.user.add_monthly_budget(amount, 1)
        assert self.user.monthly_budget == amount_valid


if __name__ == '__main__':
    unittest.main()
