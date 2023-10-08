import asyncio

from discord.ext import commands, tasks
import discord
from discordUser import User
from discord.ui import Select, View
import logging
import os
from calendar import monthrange
import pathlib
import pickle
import re
import time
import csv
import io
from datetime import datetime
from tabulate import tabulate
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

BOT_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

logger = logging.getLogger()
bot = commands.Bot(command_prefix="#", intents=discord.Intents.all())
user_list = {}
logger = logging.getLogger()

@bot.event
async def on_ready():
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! Welcome to FinBot - a simple solution to track your expenses! \n\n"
            + "Enter /menu command to view all the commands offered by FinBot")

@bot.command()
async def menu(ctx):
    """
    Handles the commands 'menu'. To show the list of available commands and their descriptions. Outputs a An embed window sent to the context 
    with all commands/descriptions

    :param ctx - Discord context window
    :type: object
    :return: None
    """

    em = discord.Embed(
        title="FinBot",
        description="Here is a list of available commands, please enter a command of your choice so that I can assist you further.\n ",
        color = discord.Color.teal()
    )
    em.add_field(name="**/menu**", value="Displays all commands and their descriptions", inline=False)
    em.add_field(name="**/add**", value="Record/Add a new spending", inline=False)
    em.add_field(name="**/display**", value="Show sum of expenditure for the current day/month", inline=False)
    em.add_field(name="**/history**", value="Display spending history", inline=False)
    em.add_field(name="**/delete**", value="Clear/Erase all your records", inline=False)
    em.add_field(name="**/edit**", value="Edit/Change spending details", inline=False)
    em.add_field(name="**/budget**", value="Set budget for the month", inline=False)
    em.add_field(name="**/chart**", value="See your expenditure in different charts", inline=False)
    
    
    await ctx.send(embed=em)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def budget(ctx):
    """
    Handles the commands 'budget'. To set a budget monthly and hence keep a track of the transactions. 

    :param ctx - Discord context window
    :type: object
    :return: None
    """
    if CHANNEL_ID not in user_list.keys():
        user_list[CHANNEL_ID] = User(CHANNEL_ID)
    try:
        await ctx.send(f"Your current monthly budget is {user_list[CHANNEL_ID].monthly_budget}")
        await ctx.send("Enter an amount to update your monthly budget. (Enter numeric values only)")
        budget = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send('You ran out of time to answer!')
    else:
        if budget:
            await post_budget_input(ctx, budget)
        else:
            await ctx.send('Nope enter a valid date')

async def post_budget_input(ctx, budget):
    try:
        amount_entered = budget.content
        amount_value = user_list[CHANNEL_ID].validate_entered_amount(
            amount_entered
        )  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Budget amount has to be a positive number.")
        user_list[CHANNEL_ID].add_monthly_budget(amount_value, CHANNEL_ID)
        await ctx.send(f"The budget for this month has been set as $ {amount_value}")
    
    except Exception as ex:
        await ctx.send("Oh no! " + str(ex))
        budget = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if budget.content.isnumeric():
            await post_budget_input(ctx, budget)
        elif '/' not in budget.content :
            await ctx.send("Exception received: 'budget' is not a numeric character. Please re-enter \/budget command")

async def select_date(ctx):
    await ctx.send("Enter the date (1-31):")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        date_message = await bot.wait_for('message', check=check, timeout=60)
        date = date_message.content.strip()

        await ctx.send("Enter the month (1-12):")
        month_message = await bot.wait_for('message', check=check, timeout=60)
        month = month_message.content.strip()

        await ctx.send("Enter the year (e.g., 2023):")
        year_message = await bot.wait_for('message', check=check, timeout=60)
        year = year_message.content.strip()

        # Call the next function with the date, month, and year
        await process_date(ctx, date, month, year)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")

async def process_date(ctx, date, month, year):
    # Process the date, month, and year here
    # You can perform any necessary calculations or operations
    # For example, you can convert them to a datetime object
    try:
        date_obj = datetime(int(year), int(month), int(date))
        await ctx.send(f"Selected Date: {date_obj.strftime('%Y-%m-%d')}")
        await select_category(ctx, date_obj)
    except ValueError:
        await ctx.send("Invalid date, month, or year. Please enter valid values.")

@bot.command()
async def add(ctx):
    '''
    Transactions stored like 'Food': [{'Date': '10032023', 'Value': '150'}] in transactions dictionary.
    '''
    if CHANNEL_ID not in user_list.keys():
        user_list[CHANNEL_ID] = User(CHANNEL_ID)
    try:
        await select_date(ctx)

    except Exception as ex:
        print("Exception occurred : ")
        print(str(ex), exc_info=True)
        await ctx.send("Processing Failed - \nError : " + str(ex))

async def select_category(ctx, date):
    '''
    Function to enable category selection via a custom defined category dropdown. This function is invoked from the select_date to 
    select the category of expense to be added. Uses the Select and View classes from discord.ui and a callback to handle the
    interaction response

    :param ctx - Discord context window
    :param Bot - Discord Bot object
    :param date - date message object received from the user 
    :type: object
    :return: None

    '''

    spend_categories = user_list[CHANNEL_ID].spend_categories
    global selected_category
    selected_category = ''
    select_options = [
        discord.SelectOption(
                label=category,
        ) for category in spend_categories
    ]
    select = Select(placeholder="Select a category", max_values=1,min_values=1, options=select_options)
    
    async def my_callback(interaction):
        await interaction.response.send_message(f'You chose: {select.values[0]}')
        await asyncio.sleep(0.5)

        if select.values[0] not in spend_categories:
            await ctx.send("Invalid category")   
            raise Exception(
                    'Sorry I don\'t recognise this category "{}"!'.format(select.values[0])
            )

        await post_category_selection(ctx, date, select.values[0])
   
    select.callback = my_callback
    view = View(timeout=90)
    view.add_item(select)
  
    await ctx.send('Please select a category', view=view)

async def post_category_selection(ctx, date_to_add,category):
    """
    Receives the category selected by the user and then asks for the amount spend. If an invalid category is given,
    an error message is displayed followed by command list. IF the category given is valid, 'post_amount_input' is
    called next.

    :param message: telebot.types.Message object representing the message object
    :param date_to_add: the date of the purchase
    :type: object
    :return: None
    """
    try:
        selected_category = category
        
        await ctx.send(f'how much did you spend on {selected_category}')
        amount = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

        await post_amount_input(ctx, amount.content,selected_category,date_to_add)
    except Exception as ex:
        await ctx.send(f"{ex}")
        

async def post_amount_input(ctx, amount_entered,selected_category,date_to_add):
    """
    Receives the amount entered by the user and then adds to transaction history. An error is displayed if the entered
     amount is zero. Else, a message is shown that the transaction has been added.

    :param date_of_entry: user entered date
    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    try:
        print(amount_entered,selected_category,date_to_add)
        amount_value = user_list[CHANNEL_ID].validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending

            raise Exception("Spent amount has to be a non-zero number.")

        category_str, amount_str = (
            selected_category,
            format(amount_value, ".2f"),
        )
        user_list[CHANNEL_ID].add_transaction(date_to_add, selected_category, amount_value, CHANNEL_ID)
        total_value = user_list[CHANNEL_ID].monthly_total()
        add_message = f"The following expenditure has been recorded: You have spent ${amount_entered} for {selected_category} on {date_to_add}"

        if user_list[CHANNEL_ID].monthly_budget > 0:
            if total_value > user_list[CHANNEL_ID].monthly_budget:
                await ctx.send("*You have gone over the monthly budget*")
            elif total_value == user_list[CHANNEL_ID].monthly_budget:
                await ctx.send("*You have exhausted your monthly budget. You can check/download history*")
            elif total_value >= 0.8 * user_list[CHANNEL_ID].monthly_budget:
                await ctx.send("*You have used 80% of the monthly budget*")

        await ctx.send(add_message)
    except Exception as ex:

        print("Exception occurred : ")
        logger.error(str(ex), exc_info=True)
        await ctx.send(f"Processing Failed - \nError : " + str(ex))

@bot.command()
async def delete(ctx):
    """
    Handles the 'delete' command. The user is then given 3 options, 'day', 'month' and 'All" from which they can choose.
    An error message is displayed if there is no transaction history. If there is transaction history, the execution is
    passed to the function 'process_delete_argument'.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """
    dateFormat = "%m-%d-%Y"
    monthFormat = "%m-%Y"
    try:
        if (CHANNEL_ID in user_list
            and user_list[CHANNEL_ID].get_number_of_transactions() != 0):
            
            curr_day = datetime.now()
            prompt = "Enter the day, month, or All\n"
            prompt += f"\n\tExample day: {curr_day.strftime(dateFormat)}\n"
            prompt += f"\n\tExample month: {curr_day.strftime(monthFormat)}"
            await ctx.send(prompt)
            delete_type = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            await process_delete_argument(ctx, delete_type.content)
        else:
            delete_history_text = (
                "No records to be deleted. Start adding your expenses to keep track of your "
                "spendings! "
            )
            await ctx.send(delete_history_text)

    except Exception as ex:
        print("Exception occurred : ")
        logger.error(str(ex), exc_info=True)
        await ctx.send("Processing Failed - \nError : " + str(ex))


async def process_delete_argument(ctx, delete_type):
    """
    This function receives the choice that user inputs for delete and asks for a confirmation. 'handle_confirmation'
    is called next.

    :param message: telebot.types.Message object representing the message object
    :type: object
    :return: None
    """

    dateFormat = "%m-%d-%Y"
    monthFormat = "%m-%Y"
    text = delete_type #delete_type
    ctx = ctx
    date = None
    is_month = False
    if text.lower() == "all":
        date = "all"
    else:
        # try and parse as Date-Month-Year
        if user_list[CHANNEL_ID].validate_date_format(text, dateFormat) is not None:
            print("date_format check")
            date = user_list[CHANNEL_ID].validate_date_format(text, dateFormat)
            print(date)
        # try and parse as Month-Year
        elif user_list[CHANNEL_ID].validate_date_format(text, monthFormat) is not None:
            print("month_format check")
            date = user_list[CHANNEL_ID].validate_date_format(text, monthFormat)
            is_month = True

    if date is None:
        # if none of the formats worked
        await ctx.send("error parsing text")
    else:
        # get the records either by given day, month, or all records
        records_to_delete = user_list[CHANNEL_ID].get_records_by_date(date, is_month)
        # if none of the records match that day
        if len(records_to_delete) == 0:
            await ctx.send(f"No transactions within {text}")
        response_str = "Confirm records to delete\n"
        response_str += user_list[CHANNEL_ID].display_transaction(records_to_delete)
        await ctx.send(response_str)
        response_str = "\nEnter Yes or No"
        await ctx.send(response_str)
        response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await handle_confirmation(ctx, response.content, records_to_delete)


async def handle_confirmation(ctx, message, records_to_delete):
    """
    Deletes the transactions in the previously chosen time period if the user chooses 'yes'.

    :param message: telebot.types.Message object representing the message object
    :param records_to_delete: the records to remove
    :type: object
    :return: None
    """

    if message.lower() == "yes":
        user_list[CHANNEL_ID].deleteHistory(records_to_delete)
        user_list[CHANNEL_ID].save_user(CHANNEL_ID)
        await ctx.send("Successfully deleted records")
    else:
        await ctx.send("No records deleted")

@bot.command()
async def chart(ctx):
    if CHANNEL_ID not in user_list.keys():
        user_list[CHANNEL_ID] = User(CHANNEL_ID)

    try:
        await ctx.send("Please enter the start date (YYYY-MM-DD):")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        start_date_message = await bot.wait_for('message', check=check, timeout=30)
        start_date_str = start_date_message.content

        await ctx.send("Please enter the end date (YYYY-MM-DD):")

        end_date_message = await bot.wait_for('message', check=check, timeout=30)
        end_date_str = end_date_message.content

        start_date_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date_str, "%Y-%m-%d")

        chart_file = user_list[CHANNEL_ID].create_chart(CHANNEL_ID, start_date_dt, end_date_dt)
        for cf in chart_file:
            with open(cf, "rb") as f:
                file = discord.File(f)
                await ctx.send(file=file)

    except Exception as ex:
        print("Exception occurred : ")
        print(str(ex), exc_info=True)
        await ctx.send("Processing Failed - \nError : " + str(ex))

def get_users():
    """
    Reads data and returns user list as a Dict

    :return: users
    :rtype: dict
    """

    data_dir = "discordData"
    users = {}
    for file in os.listdir(data_dir):
        if file.endswith(".pickle"):
            u = re.match(r"(.+)\.pickle", file)
            if u:
                u = u.group(1)
                abspath = pathlib.Path("{0}/{1}".format(data_dir, file)).absolute()
                with open(abspath, "rb") as f:
                    users[u] = pickle.load(f)
    return users


if __name__ == "__main__":
    try:
        user_list = get_users()
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"{e}")

