import discord
from discord.ext import commands, tasks
import asyncio

class SpeechCog(commands.Cog):
    """SpeechCog"""

    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.server = None
        self.vc = None

        self._autoleave.start()

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

    @commands.command(name='dadaa')
    async def _dadaa(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """ Joins, says Kan I Se Det and leaves again """
        if ctx.message.author.voice:
            self.channel = ctx.message.author.voice.channel
            self.vc      = await self.channel.connect()
            self.server  = ctx.message.guild.voice_client

            self.vc.play(discord.FFmpegPCMAudio('dadaa.mp4'), after=lambda e: print('done', e))
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

    @tasks.loop(seconds=15)
    async def _autoleave(self):
        #Leaves automatically if Michael is not saying anything.
        try:
            if self.channel is not None:
                if self.vc is None or not self.vc.is_playing():
                    print('The bot should leave.')
                await self.server.disconnect()
                self.vc = None
                self.channel = None
        except:
            print('The bot should not leave.')

def setup(bot):
    bot.add_cog(SpeechCog(bot))
