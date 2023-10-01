from discord.ext import commands, tasks
import discord

BOT_TOKEN = "MTE1ODExODc0MjQ0Njg0MjA3Nw.GF2K-g.Ft-OZz1oODvfZwY6yHjMrEY4BXlAf_gAmeHxwU"
CHANNEL_ID = 1158122419660275875

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello! FinBot is ready")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Welcome to FinBot!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, x, y):
    result = int(x) + int(y)
    await ctx.send(f"{x} + {y} = {result}")

bot.run(BOT_TOKEN)