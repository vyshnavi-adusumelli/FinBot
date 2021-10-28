"""

File contains bot message handlers and their associated functions

"""
import json
import logging
import re
import os
import sys

import telebot
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import pickle

from user import User

api_token = "INSERT API KEY HERE"
commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'display': 'Show sum of expenditure for the current day/month',
    'history': 'Display spending history',
    'delete': 'Clear/Erase all your records',
    'edit': 'Edit/Change spending details',
    'budget': 'Set budget for the month'
}

bot = telebot.TeleBot(api_token)
telebot.logger.setLevel(logging.INFO)
user_list = {}
option = {}
logger = logging.getLogger()

@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    """
    Handles the commands 'start' and 'menu'. Sends an intro text.

    :param m: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    chat_id = m.chat.id
    text_intro = "Welcome to TrackMyDollar - a simple solution to track your expenses! \nHere is a list of available " \
                 "commands, please enter a command of your choice so that I can assist you further: \n\n "
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)


@bot.message_handler(commands=['budget'])
def command_budget(message):
    """
    Handles the commands 'budget'. Gets input for budget and stores it.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    global option
    chat_id = str(message.chat.id)
    option.pop(chat_id, None)
    if chat_id not in user_list.keys():
        user_list[chat_id] = User(chat_id)
    message = bot.send_message(chat_id, 'How much is your monthly budget? \n(Enter numeric values only)')
    bot.register_next_step_handler(message, post_budget_input)

def post_budget_input(message):
    """
    Receives the amount entered by the user and then adds it to the monthly_budget attribute of the user object. An error is displayed if the entered amount is zero. Else, a message is shown that the budget has been added.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    try:
        chat_id = str(message.chat.id)
        amount_entered = message.text
        amount_value = user_list[chat_id].validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Budget amount has to be a non-zero number.")
        user_list[chat_id].add_monthly_budget(amount_value, chat_id)
        bot.send_message(chat_id, 'The budget for this month has been set as ${}'.format(str(amount_value)))

    except Exception as e:
        bot.reply_to(message, 'Oh no. ' + str(e))

@bot.message_handler(commands=['add'])
def command_add(message):
    """
    Handles the command 'add'. Lists the categories from which the user can select. The function 'post_category_selection' is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    global option
    chat_id = str(message.chat.id)
    option.pop(chat_id, None)
    if chat_id not in user_list.keys():
        user_list[chat_id] = User(chat_id)
    spend_categories = user_list[chat_id].spend_categories
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in spend_categories:
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection)


def post_category_selection(message):
    """
    Receives the category selected by the user and then asks for the amount spend. If an invalid category is given, an error message is displayed followed by command list. IF the category given is valid, 'post_amount_input' is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global option
    global user_list
    try:
        chat_id = str(message.chat.id)
        selected_category = message.text
        spend_categories = user_list[chat_id].spend_categories
        if not selected_category in spend_categories:
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))

        option[chat_id] = selected_category
        message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only)'.format(
            str(option[chat_id])))
        bot.register_next_step_handler(message, post_amount_input)
    except Exception as e:
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def post_amount_input(message):
    """
    Receives the amount entered by the user and then adds to transaction history. An error is displayed if the entered amount is zero. Else, a message is shown that the transaction has been added.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    global option
    dateFormat = '%d-%m-%Y'
    timeFormat = '%H:%M'
    monthFormat = '%m-%Y'
    try:
        chat_id = str(message.chat.id)
        amount_entered = message.text
        amount_value = user_list[chat_id].validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = datetime.today()
        date_str, category_str, amount_str = str(date_of_entry), str(option[chat_id]), str(amount_value)
        user_list[chat_id].add_transaction(date_of_entry, option[chat_id], amount_value, chat_id)
        total_value = user_list[chat_id].monthly_total()
        add_message = 'The following expenditure has been recorded: You have spent ${} for {} on {}'.format(
            amount_str, category_str, date_str, total_value)

        if total_value > user_list[chat_id].monthly_budget:
            bot.send_message(chat_id, text="*You have gone over the monthly budget*",
                             parse_mode='Markdown')
        elif total_value >= 0.8*user_list[chat_id].monthly_budget:
            bot.send_message(chat_id, text="*You have used 80% of the monthly budget.*",
                         parse_mode='Markdown')
        bot.send_message(chat_id, add_message)


    except Exception as e:
        print("Exception occurred : ")
        logger.error(str(e), exc_info=True)
        bot.reply_to(message, 'Processing Failed - \nError : ' + str(e))


@bot.message_handler(commands=['history'])
def show_history(message):
    """
    Handles the command 'history'. Lists the transaction history.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    try:
        chat_id = str(message.chat.id)
        spend_total_str = ""
        if chat_id not in list(user_list.keys()):
            raise Exception("Sorry! No spending records found!")
        spend_history_str = "Here is your spending history : \nDATE, CATEGORY, AMOUNT\n----------------------\n"
        if len(user_list[chat_id].transactions) == 0:
            spend_total_str = "Sorry! No spending records found!"
        else:
            for category in user_list[chat_id].transactions.keys():
                for transaction in user_list[chat_id].transactions[category]:
                    date = str(transaction["Date"])
                    value = str(transaction["Value"])
                    spend_total_str += "Category: {} Date: {} Value: {} \n".format(category, date, value)
            bot.send_message(chat_id, spend_history_str + spend_total_str)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        bot.reply_to(message, "Oops!" + str(e))


@bot.message_handler(commands=['display'])
def command_display(message):
    """
    Handles the command 'display'. If the user has no transaction history, a message is displayed. If there is transaction history, user is given choices of time periods to choose from. The function 'display_total' is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    global option
    chat_id = str(message.chat.id)
    if chat_id not in user_list or user_list[chat_id].get_number_of_transactions() == 0:
        bot.send_message(chat_id, "Oops! Looks like you do not have any spending records!")
    else:
        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 2
            for mode in user_list[chat_id].spend_display_option:
                markup.add(mode)
            msg = bot.reply_to(message, 'Please select a category to see the total expense', reply_markup=markup)
            bot.register_next_step_handler(msg, display_total)

        except Exception as e:
            print("Exception occurred : ")
            logger.error(str(e), exc_info=True)
            bot.reply_to(message, 'Oops! - \nError : ' + str(e))


def display_total(message):
    """
    Receives the input time period and displays the transaction summary for the corresponding time period.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    dateFormat = '%d/%m/%Y'
    timeFormat = '%H:%M'
    monthFormat = '%m/%Y'
    try:
        chat_id = str(message.chat.id)
        day_week_month = message.text

        if not day_week_month in user_list[chat_id].spend_display_option:
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(day_week_month))

        if len(user_list[chat_id].transactions) == 0:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")

        if day_week_month == 'Day':
            query = datetime.today()
            query_result = ""
            total_value = 0
            for category in user_list[chat_id].transactions.keys():
                for transaction in user_list[chat_id].transactions[category]:
                    if transaction["Date"].strftime("%d") == query.strftime("%d"):
                        query_result += "Category {} Date {} Value {} \n".format(category, transaction["Date"].strftime(
                            dateFormat), transaction["Value"])
                        total_value += transaction["Value"]
            total_spendings = "Here are your total spendings for the date {} \n".format(
                datetime.today().strftime("%d-%m-%Y"))
            total_spendings += query_result
            total_spendings += "Total Value {}".format(total_value)
            bot.send_message(chat_id, total_spendings)
        elif day_week_month == 'Month':
            query = datetime.today()
            query_result = ""
            total_value = 0
            # print(user_list[chat_id].keys())
            budget_value = user_list[chat_id].monthly_budget
            for category in user_list[chat_id].transactions.keys():
                for transaction in user_list[chat_id].transactions[category]:
                    if transaction["Date"].strftime("%m") == query.strftime("%m"):
                        query_result += "Category {} Date {} Value {} \n".format(category, transaction["Date"].strftime(
                            dateFormat), transaction["Value"])
                        total_value += transaction["Value"]
            total_spendings = "Here are your total spendings for the Month {} \n".format(
                datetime.today().strftime("%m"))
            total_spendings += query_result
            total_spendings += "Total Value {}\n".format(total_value)
            total_spendings += "Budget for the month {}".format(str(budget_value))
            bot.send_message(chat_id, total_spendings)
    except Exception as e:
        print("Exception occurred : ")
        logger.error(str(e), exc_info=True)
        bot.reply_to(message, str(e))


@bot.message_handler(commands=['edit'])
def edit1(message):
    """
    Handles the command 'edit' and then displays a message explaining the format. The function 'edit2' is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    global option
    chat_id = str(message.chat.id)

    if chat_id in list(user_list.keys()):
        msg = bot.reply_to(message, "Please enter the date, category and value of the transaction you made (Eg: "
                                    "01/03/2021,Transport,25)")
        bot.register_next_step_handler(msg, edit2)

    else:
        bot.reply_to(chat_id, "No data found")


def edit2(message):
    """
    Receives the transaction to be edited, and then asks the user what they want to edit. The function 'edit3' is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """

    chat_id = str(message.chat.id)
    info = message.text
    info = info.split(',')
    try:
        info_date = datetime.strptime(info[0].strip(), "%m/%d/%Y")
        info_category = info[1].strip()
        info_value = info[2].strip()
        if info_date is None:
            bot.reply_to(message, "The date is incorrect")
            return
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        choices = ['Date', 'Category', 'Cost']
        for c in choices:
            markup.add(c)

        for transaction in user_list[chat_id].transactions[info_category]:
            if transaction["Date"].date() == info_date.date():
                if str(int(transaction["Value"])) == info_value:
                    user_list[chat_id].store_edit_transaction(transaction, info_category)
                    choice = bot.reply_to(message, "What do you want to update?", reply_markup=markup)
                    bot.register_next_step_handler(choice, edit3)
                    break

    except Exception as e:
        print("Exception occurred : ")
        logger.error(str(e), exc_info=True)
        bot.reply_to(message, "Processing Failed - \nError : Incorrect format - (Eg: 01/03/2021,Transport,25)")


def edit3(message):
    """
    Receives the user's input corresponding to what they want to edit, and then transfers the execution to the function according to the choice.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    choice1 = message.text
    chat_id = str(message.chat.id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for category in user_list[chat_id].spend_categories:
        markup.add(category)
    if choice1 == 'Date':
        new_date = bot.reply_to(message, "Please enter the new date (in mm/dd/yyyy format)")
        bot.register_next_step_handler(new_date, edit_date)

    if choice1 == 'Category':
        new_cat = bot.reply_to(message, "Please select the new category", reply_markup=markup)
        bot.register_next_step_handler(new_cat, edit_cat)

    if choice1 == 'Cost':
        new_cost = bot.reply_to(message, "Please type the new cost")
        bot.register_next_step_handler(new_cost, edit_cost)


def edit_date(message):
    """
    This function is called if the user chooses to edit the date of a transaction. This function receives the new date and updates the transaction.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    new_date = message.text
    chat_id = str(message.chat.id)
    user_date = datetime.strptime(new_date, "%m/%d/%Y")
    if user_date is None:
        bot.reply_to(message, "The date is incorrect")
        return
    updated_transaction = user_list[chat_id].edit_transaction_date(user_date)
    user_list[chat_id].save_user(chat_id)
    edit_message = "Date is updated. Here is the new transaction. \n Date {}. Value {}. \n".format(
        updated_transaction["Date"], updated_transaction["Value"])
    bot.reply_to(message, edit_message)


def edit_cat(message):
    """
    This function is called if the user chooses to edit the category of a transaction. This function receives the new category and updates the transaction.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    chat_id = str(message.chat.id)
    new_category = message.text.strip()
    updated_transaction = user_list[chat_id].edit_transaction_category(new_category)
    if updated_transaction:
        user_list[chat_id].save_user(chat_id)
        edit_message = "Category has been edited."
        bot.reply_to(message, edit_message)
    else:
        edit_message = "Category has not been edited successfully"
        bot.reply_to(message, edit_message)


def edit_cost(message):
    """
    This function is called if the user chooses to edit the amount of a transaction. This function receives the new amount and updates the transaction.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    new_cost = message.text
    chat_id = str(message.chat.id)
    new_cost = user_list[chat_id].validate_entered_amount(new_cost)
    if new_cost != 0:
        user_list[chat_id].save_user(chat_id)
        updated_transaction = user_list[chat_id].edit_transaction_value(new_cost)
        edit_message = "Value is updated. Here is the new transaction. \n Date {}. Value {}. \n".format(
            updated_transaction["Date"], updated_transaction["Value"])
        bot.reply_to(message, edit_message)

    else:
        bot.reply_to(message, "The cost is invalid")
        return


@bot.message_handler(commands=['delete'])
def command_delete(message):
    """
    Handles the 'delete' command. The user is then given 3 options, 'day', 'month' and 'All" from which they can choose. An error message is displayed if there is no transaction history. If there is transaction history, the execution is passed to the function 'process_delete_argument'.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    dateFormat = '%d-%b-%Y'
    monthFormat = '%b-%Y'
    chat_id = str(message.chat.id)
    if chat_id in user_list and user_list[chat_id].get_number_of_transactions() != 0:
        curr_day = datetime.now()
        prompt = f"Enter the day, month, or All\n"
        prompt += f"\n\tExample day: {curr_day.strftime(dateFormat)}\n"
        prompt += f"\n\tExample month: {curr_day.strftime(monthFormat)}"
        reply_message = bot.reply_to(message, prompt)
        bot.register_next_step_handler(reply_message, process_delete_argument)
    else:
        delete_history_text = "No records to be deleted. Start adding your expenses to keep track of your " \
                              "spendings! "
        bot.send_message(chat_id, delete_history_text)


def process_delete_argument(message):
    """
    This function receives the choice that user inputs for delete and asks for a confirmation. 'handle_confirmation' is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list
    dateFormat = '%d-%b-%Y'
    timeFormat = '%H:%M'
    monthFormat = '%b-%Y'
    text = message.text
    chat_id = str(message.chat.id)

    date = None
    is_month = False
    if text.lower() == "all":
        date = "all"
    else:
        # try and parse as Date-Month-Year
        if user_list[chat_id].validate_date_format(text, dateFormat) is not None:
            date = user_list[chat_id].validate_date_format(text, dateFormat)
        # try and parse as Month-Year
        elif user_list[chat_id].validate_date_format(text, monthFormat) is not None:
            date = user_list[chat_id].validate_date_format(text, monthFormat)
            is_month = True

    if date is None:
        # if none of the formats worked
        bot.reply_to(message, "Error parsing date")
    else:
        # get the records either by given day, month, or all records
        records_to_delete = user_list[chat_id].get_records_by_date(date, chat_id, is_month)
        # if none of the records match that day
        if len(records_to_delete) == 0:
            bot.reply_to(message, f"No transactions within {text}")
            return
        response_str = "Confirm records to delete\n"
        response_str += user_list[chat_id].display_transaction(records_to_delete)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Yes")
        markup.add("No")
        response_str += "\nReply YES or NO"
        response = bot.reply_to(message, response_str, reply_markup=markup)
        bot.register_next_step_handler(response, handle_confirmation, records_to_delete)


def handle_confirmation(message, records_to_delete):
    """
    Deletes the transactions in the previously chosen time period if the user chooses 'yes'.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    global user_list

    chat_id = str(message.chat.id)
    if message.text.lower() == "yes":
        user_list[chat_id].deleteHistory(records_to_delete)
        user_list[chat_id].save_user(chat_id)
        bot.send_message(message.chat.id, f"Successfully deleted records")
    else:
        bot.send_message(message.chat.id, "No records deleted")


def get_users():
    """
    Reads data and returns user list as a Dict

    :return: users
    :rtype: Dict
    """
    data_dir = "../data"
    users = {}
    for file in os.listdir(data_dir):
        if file.endswith(".pickle"):
            user = re.match("(.+)\.pickle", file)
            if user:
                user = user.group(1)
                with open("{0}/{1}".format(data_dir, file), "rb") as f:
                    users[user] = pickle.load(f)
    return users


if __name__ == '__main__':
    try:
        user_list = get_users()
        bot.polling(none_stop=True)
    except Exception as e:
        #Connection will be timed out with the set time interval - 3
        time.sleep(3)
        print("Exception occurred while processing : ")
        logger.error(str(e), exc_info=True)

