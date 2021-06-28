import discord
from discord.ext import commands, tasks
import asyncio
import numpy as np
import os

class QuotesCog(commands.Cog):
    """SpeechCog"""

    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.server = None
        self.vc = None

        #self._autoleave.start()

#     @commands.command(name='join')
#     async def _join(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
#         """Summons the bot to a voice channel.
#         If no channel was specified, it joins your channel.
#         """
# 
#         if ctx.message.author.voice:
#             self.channel = ctx.message.author.voice.channel
#             self.vc = await self.channel.connect()
#             self.server = ctx.message.guild.voice_client
# 
#         else:
#             await ctx.channel.send('Du er ikke engang selv i en channel...')
    @commands.command(name='t')
    async def _t(self, ctx):
        """ Test function. """
        
        ids = []; names = [];
        for guild in self.bot.guilds:
            for member in guild.members:
                id = member.id
                name = member.name
                if member.status == discord.Status.online:
                    ids.append(id)
                    names.append(name)
        
        ids = np.unique(ids)
        names = np.unique(names)
        for id, name in zip(ids, names):
            print(f'{id} : {name}')
            
        print(f'len(id):{len(ids)}, len(names):{len(names)}')
        print(f'type(id):{type(ids[0])}, type(name):{type(names[0])}')
                
    @commands.command(name='y')
    async def _y(self, ctx):
        """ Test function 2 """
        print(ctx.message.author.id)

    @commands.command(name='p', aliases=['pl','play'])
    async def _p(self, ctx, *, arg):
        """ Plays a quote. """
        
        path = ''
        argin = ctx.message.content.replace('_mb p ','').lower()
        
        #Check if the message contains "kan i se det":
        if 'kan i se det' in argin:
            path = './resources/kanisedet/' + np.random.choice(os.listdir('./resources/kanisedet'))
        elif argin == 'aah':
            path = './resources/soundfiles/Ahh.mp4'
        else:
            print('Unknown quote.')
        
        #Play the audio
        if ctx.message.author.voice and path != '':
            self.channel = ctx.message.author.voice.channel
            self.vc      = await self.channel.connect()
            self.server  = ctx.message.guild.voice_client

            self.vc.play(discord.FFmpegPCMAudio(path))
            while self.vc.is_playing():
                await asyncio.sleep(1)

            self.vc.stop()
            await ctx.voice_client.disconnect()
        
            
            
            
            
            
#     @commands.command(name='leave', aliases=['disconnect'])
#     @commands.has_permissions(manage_guild=True)
#     async def _leave(self, ctx: commands.Context):
#         """Clears the queue and leaves the voice channel."""
# 
#         if not ctx.voice_state.voice:
#             return await ctx.send('Not connected to any voice channel.')
# 
#         await ctx.voice_state.stop()
#         del self.voice_states[ctx.guild.id]

#     @tasks.loop(seconds=15)
#     async def _autoleave(self):
#         #Leaves automatically if Michael is not saying anything.
#         try:
#             if self.channel is not None:
#                 if self.vc is None or not self.vc.is_playing():
#                     print('The bot should leave.')
#                 await self.server.disconnect()
#                 self.vc = None
#                 self.channel = None
#         except:
#             print('The bot should not leave.')

def setup(bot):
    bot.add_cog(QuotesCog(bot))
