from discord.ext import commands, tasks
import discord
from discordUser import User
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

'''

Class defining the category dropdown and the callback function
which deals with the response from the interaction

'''
class Select(discord.ui.Select):
    def __init__(self, categories):    
        select_options = [
            discord.SelectOption(
                label=category,
            ) for category in categories
        ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=select_options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Your choice is {self.values[0]}!",ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, categories):
        super().__init__()
        self.add_item(Select(categories))


@bot.event
async def on_ready():
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! Welcome to FinBot - a simple solution to track your expenses! \n\n"
            + "Enter menu command to view all the commands offered by FinBot")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx):
    '''
    Category should be spelled exactly matching with one of the below:
    "Food",
    "Groceries",
    "Utilities",
    "Transport",
    "Shopping",
    "Miscellaneous",

    Transactions stored like 'Food': [{'Date': '10032023', 'Value': '150'}] in transactions dictionary.
    '''
    if CHANNEL_ID not in user_list.keys():
        user_list[CHANNEL_ID] = User(CHANNEL_ID)
    try:
        await select_date(ctx, bot)

    except Exception as ex:
        print("Exception occurred : ")
        print(str(ex), exc_info=True)
        await ctx.send("Processing Failed - \nError : " + str(ex))

async def select_date(ctx, bot):
    '''
    Function to enable date selection via a custom defined calendar widget. This function is invoked from the add command to select the date of
    expense to be added. This function further invokes select_category function by passing the date, context object and bot object.

    :param ctx - Discord context window
    :param Bot - Discord Bot object
    :type: object
    :return: None

    '''

    # Logic to make the bot wait for user response
    await ctx.send('Please choose the date')

    # waits for a message response - for now enter 10032023 format ; Needs to be updated with calendar dropdown and date checking logic as in the telebot.py
    date = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    # Modify this logic to verify the date selected is in proper format and then proceed with category selection
    if date:
        await select_category(ctx, bot, date)
    else:
        await ctx.send('Nope enter a valid date')

async def select_category(ctx, bot, date):
    '''
    Function to enable category selection via a custom defined category dropdown. This function is invoked from the select_date to 
    select the category of expense to be added. 

    :param ctx - Discord context window
    :param Bot - Discord Bot object
    :param date - date message object received from the user 
    :type: object
    :return: None

    '''

    spend_categories = list(user_list[CHANNEL_ID].spend_categories)
    # Logic to make the bot wait for user response
    await ctx.send('Categories!', view=SelectView(spend_categories))

    #await ctx.send('Please enter the category')
    #category = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    #await ctx.send('Please enter the amount')
    #amount = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    #print(date.content, category.content, amount.content)
    #user_list[CHANNEL_ID].add_transaction(date.content, category.content, amount.content,CHANNEL_ID)
    # await ctx.send("transaction added!")

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