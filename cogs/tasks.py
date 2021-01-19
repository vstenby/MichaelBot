import discord
from discord.ext import commands, tasks
import asyncio

import numpy

class TasksCog(commands.Cog):
    """SpeechCog"""
    
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.server = None
        self.vc = None

        self._bob.start()


    @tasks.loop(seconds=15)
    async def _bob(self):
        #Changes Michael's Status every 5 minutes.
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='01005_' + str(numpy.random.randint(5))))


def setup(bot):
    bot.add_cog(TasksCog(bot))

