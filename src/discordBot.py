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

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
user_list = {}
logger = logging.getLogger()

@bot.event
async def on_ready():
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! Welcome to FinBot - a simple solution to track your expenses! \n\n"
            + "Enter menu command to view all the commands offered by FinBot")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

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

def get_users():
    """
    Reads data and returns user list as a Dict

    :return: users
    :rtype: dict
    """

    data_dir = "data"
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

