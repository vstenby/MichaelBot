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
        self.vc = ''
        self.queue = []
        self.channel = ''


    #Commands from the Music cog.
    @commands.command(brief='Play music through YouTube.',
                      description="MichaelBot's YouTube-player.\nUsage: _mb yt <url> or _mb yt <search phrase>")
    async def p(self, ctx):
        add_to_queue = False
        msg = ctx.message.content
        #Removing the yt command from the message.
        msg = ' '.join(msg.split(' ')[1:])
        if 'queue' or 'q ' in msg.lower():
            #If the command is <prefix> yt <queue/q> <url/search>, then it should be added to the queue.
            add_to_queue = True
            msg = ' '.join(msg.split(' ')[1:])
        elif 'skip ' or 'skip' in msg.lower():
            print('Skip.')
            msg = ' '.join(msg.split(' ')[1:])
            if self.channel != '': self.vc.stop()


        url, song_id = get_youtube_id(msg)
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
            if add_to_queue:
                #Then the song should be added to the queue.
                add_to_queue(ID)
                msg = custom_msg('music_in_queue')
                await ctx.channel.send(msg)
        else:
            if not song_there:
                wait_msg = custom_msg('download_song')
                await ctx.send(wait_msg)
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                except DownloadError:
                    await ctx.send('Desværre - den måtte jeg ikke downloade...')
            self.channel = ctx.message.author.voice.channel
            self.vc = await self.channel.connect()
            await ctx.channel.send('**Afspiller: ' + url + '**')
            self.vc.play(discord.FFmpegPCMAudio(song_path), after=lambda e: print('done', e))
            while self.vc.is_playing():
                await asyncio.sleep(1)
            self.vc.stop()
            self.channel = ''
            self.vc = ''
            await ctx.voice_client.disconnect()

    @commands.command(aliases=['P', 'play'], brief='Play various small clips in the voice channel.')
    async def mp3(self, ctx, *, arg):
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
        elif arg.lower() == 'list':
            #Display the lists of mp3s to be played.
            await ctx.channel.send(mp3s)
        else:
            msg = custom_msg('unknown_mp3')
            await ctx.channel.send(msg)

    @commands.command(brief = 'Skips the current song')
    async def skip(self, ctx):
    @commands.command()
    async def status(self, ctx):
        print(self.client)
        print(self.vc)
        print(self.queue)
        print(self.channel)



def setup(client):
    client.add_cog(Music(client))
