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

@bot.event
async def on_ready():
    print("Hello! FinBot is ready")
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! Welcome to FinBot!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, date, category, amount):
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
    user_list[CHANNEL_ID].add_transaction(date,category,amount,CHANNEL_ID)
    await ctx.send("transaction added!")

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