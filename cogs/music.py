#Dependencies for the music cog.
import discord
from discord.ext import commands
import youtube_dl
from discord.utils import get
import asyncio
from functions import *

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Commands from the Music cog.
    @commands.command(brief='Play music through YouTube.',
                      description="MichaelBot's YouTube-player.\nUsage: _mb yt <url> or _mb yt <search phrase>")
    async def yt(self, ctx):
        url, song_id = get_youtube_id(ctx.message.content)
        song_path = './resources/yt/' + song_id + '.mp3'
        song_there = os.path.isfile(song_path)
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl' : song_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if is_connected(ctx):
            msg = custom_msg('music_already_playing')
            await ctx.channel.send(msg)
        else:
            if not song_there:
                wait_msg = stream_wait_msg()
                await ctx.send(wait_msg)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            await ctx.channel.send('**Afspiller: ' + url + '**')
            vc.play(discord.FFmpegPCMAudio(song_path), after=lambda e: print('done', e))
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await ctx.voice_client.disconnect()

    @commands.command(aliases=['P', 'play'], brief='Play various small clips in the voice channel.')
    async def p(self, ctx, *, arg):
        mp3s = load_mp3s()
        mp3 = str_to_mp3(arg, mp3s)
        if mp3 != '':
            #Send gifs based on the songs.
            if 'motoriske' in mp3: await ctx.channel.send(file=discord.File('./resources/gif/matrix.gif'))
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(mp3), after=lambda e: print('done', e))
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await ctx.voice_client.disconnect()
        else:
            msg = custom_msg('unknown_mp3')
            await ctx.channel.send(msg)

def setup(client):
    client.add_cog(Music(client))
