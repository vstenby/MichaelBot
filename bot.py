# bot.py
import os
from dotenv import load_dotenv

from discord.ext import commands
import sys, traceback

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import discord
from discord.ext import commands

import sys, traceback

bot = commands.Bot(command_prefix='_mb ', description='Michael Bot')

#Load all of the extensions.
#if __name__ == '__main__':
#    for extension in cogs:
#        bot.load_extension(extension)

@bot.event
async def on_ready():

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="01005B."))
    
    
    
    
bot.run(TOKEN, bot=True, reconnect=True)
