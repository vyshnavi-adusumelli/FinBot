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
import telebot
from telebot import types
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


BOT_TOKEN = "MTE1ODExOTk0OTYyNjI1NzU0MA.GgY8T6.DVdj9Ohwb8lFOK6JKktCYJPjccaFzqxtmCENP8"
CHANNEL_ID = "1158122372524691488"

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
#user_list = {}

@bot.event
async def on_ready():
    print("Hello! FinBot is ready")
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! Welcome to FinBot!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, x, y):
    result = int(x) + int(y)
    if CHANNEL_ID not in user_list.keys():
        user_list[CHANNEL_ID] = User(CHANNEL_ID)
    print(f"{user_list[CHANNEL_ID].monthly_budget}")
    user_list[CHANNEL_ID].monthly_budget += result
    print(f"{user_list[CHANNEL_ID].monthly_budget}")
    user_list[CHANNEL_ID].save_user(CHANNEL_ID)

    await ctx.send(f"{user_list[CHANNEL_ID].monthly_budget}")

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
                    print(f"{users[u]}")
    return users


if __name__ == "__main__":
    global user_list
    user_list = {}
    try:
        user_list = get_users()
        print(user_list)
        print(f"{user_list[str(CHANNEL_ID)].monthly_budget}")
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"{e}")