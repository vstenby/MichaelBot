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
from mbot_auxil import *

#Set the prefix of the bot here.
prefix = '_mb '
client = commands.Bot(command_prefix = prefix)

@client.command(pass_context=True, brief='MichaelBot joins your server.')
async def join(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@client.command(aliases=['ses', 'stop'],pass_context=True, brief='MichaelBot leaves your sever')
async def leave(ctx):
    await ctx.voice_client.disconnect()

#Loads extentions (i.e. cogs)
@client.command(brief='Loads extentions')
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command(brief='Unloads extentions')
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command(brief = 'Reloads extentions')
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

#Loads all of the extentions upon starting.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('MichaelBot is online!')

#Make sure you have credentials.txt in your folder when running the bot.
#This can be gotten from Discord's developer site.
with open('credentials.txt', 'r') as file:
    credentials = file.read().replace('\n','')
    file.close()

client.run(credentials)
