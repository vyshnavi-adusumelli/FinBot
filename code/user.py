import os
import pickle
import re
from datetime import datetime



class User:

    def __init__(self, userid):
        self.spend_categories = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
        self.spend_display_option = ['Day', 'Month']
        self.save_user(userid)
        self.transactions = {}
        self.edit_transactions = {}
        self.edit_category = {}
        self.monthly_budget = 0


        for category in self.spend_categories:
            self.transactions[category] = []

    def save_user(self, userid):
        data_dir = "../data"
        with open("{}/{}.pickle".format(data_dir, userid), "wb") as f:
            pickle.dump(self, f)

    def validate_entered_amount(self, amount_entered):
        if 0 < len(amount_entered) <= 15:
            if amount_entered.isdigit:
                if re.match("^[0-9]*\\.?[0-9]*$", amount_entered):
                    amount = round(float(amount_entered), 2)
                    if amount > 0:
                        return amount
        return 0

    def add_transaction(self, date, category, value, userid):
        self.transactions[category].append({"Date": date, "Value": value})
        self.save_user(userid)

    def store_edit_transaction(self, existing_transaction, edit_category):
        self.edit_transactions = existing_transaction
        self.edit_category = edit_category

    def edit_transaction_date(self, new_date):
        new_date_object = datetime.strptime(new_date, "%d/%m/%Y")
        for transaction in self.transactions[self.edit_category]:
            if transaction == self.edit_transactions:
                transaction["Date"] = new_date_object
                break
        return transaction

    def edit_transaction_category(self, new_category):
        self.transactions[self.edit_category].remove(self.edit_transactions)
        self.transactions[new_category].append(self.edit_transactions)
        return True

    def edit_transaction_value(self, new_value):
        for transaction in self.transactions[self.edit_category]:
            if transaction == self.edit_transactions:
                transaction["Value"] = new_value
                break
        return transaction

    def deleteHistory(self, records=None):
        # if there are specific records to delete
        # and it is not all records from the user
        if records is not None and self.transactions != records:
            # delete only the records specified
            for category in records:
                for record in records[record]:
                    self.transactions[category].remove(record)
        else:
            self.transactions = {}
            for category in self.spend_categories:
                self.transactions[category] = []


    def validate_date_format(self, text, date_format):
        """
        Given a text, see if it is able to be formatted using the date_format
        :param text:
        :param date_format:
        :return:
        """
        date = None
        # try and parse as Month-Day-Year
        try:
            date = datetime.strptime(text, date_format).date()
        except ValueError:
            pass
        return date

    def get_records_by_date(self, date: datetime.date, chat_id: int, is_month: bool):
        """
        Given a date and chat_id returns all records that match the filter
        If is_month is true, only matches year and month, not day
        :param date:
        :param chat_id:
        :param is_month:
        :return:
        """
        dateFormat = '%d-%b-%Y'
        timeFormat = '%H:%M'
        monthFormat = '%b-%Y'
        user_history = self.transactions
        if date == "all":
            return user_history
        # else filter by date
        matched_dates = {}
        for category in self.spend_categories:
            matched_dates[category] = []
        for category in user_history:
            for record in user_history[category]:
                record_date = record['Date']
                # format it to date and time, then only get the day,month,year
                record_date = record_date.date()
                if is_month:
                    # strip the date
                    record_date = record_date.replace(day=1)
                    date = date.replace(day=1)
                # checks if the records are equal/matching
                if record_date == date:
                    matched_dates[category].append(record)
        return matched_dates


    def display_transaction(self, transaction):
        """
        Helper function to turn the dictionary into a user-readable string
        :param transaction: dictionary of category, then items
        :return:
        """
        final_str = ""

        for category in transaction:
            for record in transaction[category]:
                final_str += f'{category}, {record["Date"].date()}, {record["Value"]}\n'

        return final_str

    def get_number_of_transactions(self):
        """
        Helper function to get the total number of transactions across
        all categories
        :return: number of transactions
        """
        total = 0
        for category in self.transactions:
            for record in self.transactions[category]:
                total += len(record)
        return total

    def add_monthly_budget(self, amount, userid):
        """
        Given amount and userid, edit the budget of the current user
        :param amount: budget amount
        :param userid:
        :return:
        """
        self.monthly_budget = amount
        self.save_user(userid)

    def monthly_total(self):
        """
        Calculates total expenditure for the current month
        :return: total amount
        """
        date = datetime.today()
        query_result = ""
        total_value = 0
        for category in self.spend_categories:
            for transaction in self.transactions[category]:
                if transaction["Date"].strftime("%m") == date.strftime("%m"):
                    total_value += transaction["Value"]
        return total_value
