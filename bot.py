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

prefix = '_mb '
client = commands.Bot(command_prefix = prefix)

@client.command(pass_context=True, brief='MichaelBot joins your server.')
async def join(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@client.command(aliases=['ses', 'stop', 'Stop'],pass_context=True, brief='MichaelBot leaves your sever')
async def leave(ctx):
    await ctx.voice_client.disconnect()

#Modify the cogs.
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('MichaelBot is online!')

#Insert temp.py her

with open('credentials.txt', 'r') as file:
    credentials = file.read().replace('\n','')
    file.close()

client.run(credentials)
