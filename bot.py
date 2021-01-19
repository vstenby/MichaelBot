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

#Import cogs
cogs = ['cogs.quotes']

bot = commands.Bot(command_prefix='_mb ', description='Michael Bot')

#Load all of the extensions.
if __name__ == '__main__':
    for extension in cogs:
        bot.load_extension(extension)

@bot.event
async def on_ready():

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    #await bot.change_presence(game=discord.Game(name='Ser 01005',type=1,url='video.dtu.dk'))
    
    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="testeren"))
    #await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    #print(f'Successfully logged in and booted...!')
    
    bot.load_extension('cogs.tasks')
    
bot.run(TOKEN, bot=True, reconnect=True)
