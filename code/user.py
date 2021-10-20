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
