#Packages
import discord
from discord.ext import commands
import time
import datetime
import pandas as pd
import numpy as np
import os
import random

#Auxillary functions.
from functions import *

#Set the prefix of the bot here.
prefix = '_mb '
client = commands.Bot(command_prefix = prefix)

@client.event
async def on_member_join(member):
    print(f'Velkommen til bænken, {member}.'.encode('utf-8'))

#Loads extentions (i.e. cogs)
@client.command(brief='Loads extentions')
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(extension + ' sucessfully loaded')

@client.command(brief='Unloads extentions')
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(extension + ' sucessfully unloaded')

@client.command(brief = 'Reloads extentions')
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(extension + ' succesfully reloaded')

@client.command(brief = 'Reboots MichaelBot', hidden=True)
async def reboot(ctx):
    import sys
    print('MichaelBot is rebooting...')
    os.execv(sys.executable, ['python'] + sys.argv)

#Loads all of the extentions upon starting.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != 'game.py':
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('MichaelBot is online!')

#Make sure you have credentials.txt in your folder when running the bot.
#This is from the Discord's developer site.
with open('credentials.txt', 'r') as file:
    credentials = file.read().replace('\n','')
    file.close()

client.run(credentials)
