#Dependencies for the music cog.
import discord
from discord.ext import commands, tasks
import youtube_dl
from discord.utils import get
import asyncio
from functions import *
import asyncio
import time
import csv
import pandas as pd
from datetime import datetime

def add_points(df, members):
    #Fetches the users
    user = members
    user = [str(x) for x in members if str(x) != 'MichaelBot#8980']

    time = datetime.now()
    ts = time.strftime("%m/%d/%Y, %H:%M:%S")

    df = df.append(pd.DataFrame({'User' : user,
                            'Point' : [1] * len(user),
                            'Timestamp' : [ts] * len(user),
                            'Reason' : [''] * len(user)}))
    return df

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def MBot_fetch_song(search):
    url, song_id = get_youtube_id(search)
    song_path = './resources/yt/' + song_id + '.mp3'
    song_exist = os.path.isfile(song_path)
    #Download the YouTube url using youtube_dl.
    ydl_opts = {
        'format': 'bestaudio/best',
        'cachedir': False,
        'outtmpl' : song_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    if not song_exist:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    return url, song_path

#Clears the queue upon startup.
clear_queue()

#Audio class
class MBot_Audio(commands.Cog):
    def __init__(self,path):
        self.path = path

    def play(self,vc):
        #Plays the song
        vc.play(discord.FFmpegPCMAudio(self.path), after=lambda e: print('Played ', self.path))

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.vc = None
        self.channel = None
        self.is_playing = False
        self.play_music.start()
        self.counter = 0
        self.server = None
        self.pointcounter = 1
        self.df = load_points()
        self.save.start()


    @commands.command(brief='MichaelBot joins your server.')
    async def join(self, ctx):
        if ctx.message.author.voice:
            self.channel = ctx.message.author.voice.channel
            await self.channel.connect()
            self.server = ctx.message.guild.voice_client
        else:
            await ctx.channel.send('Du er ikke engang selv i en channel...')
            #The bot should type that a channel needs to be joined.

    @commands.command(aliases=['ses', 'stop'], brief='MichaelBot leaves your sever')
    async def leave(self,ctx):
        if self.channel is not None:
            self.channel = None
            await self.server.disconnect()
            self.server = None
            if self.vc is not None: self.vc = None
        clear_queue()

    @commands.command(aliases=['q'], brief='Add a song to your current queue.')
    async def queue(self, ctx, *args):
        #Adds a song to the queue.
        if len(args) == 1:
            args = args[0]
        else:
            args = ' '.join(args)
        url, path = MBot_fetch_song(args)
        await ctx.channel.send(url + ' er nu i queue!')
        add_to_queue(path)
        print(url + ' added to queue.')

    
    @commands.command(brief = 'Gamble your hard earned MichaelBucks')
    async def gamble(self, ctx, arg):
        
        if arg == 'all': arg = bank(str(ctx.author), self.df)
    
        #Try to check if the argument is between 0 and 1.
        #try:
        #    arg = float(arg)
        #    if 0 < arg and arg < 1:
        #        arg = arg * bank(str(ctx.author), self.df)
            
                
        
        try:
            n = int(arg)
            if n <= 0:
                await ctx.channel.send('Du kan ikke gamble et negativt antal.')
                return

            self.df, val = gamble(str(ctx.author), self.df, n)
            if val is None:
                await ctx.channel.send('Du kan ikke gamble med så meget.')
            elif val is True:
                #The bet is won
                await ctx.channel.send('Tillykke, du har vundet ' + str(n) + ' MichaelBucks.')
            elif val is False:
                #The bet is lost
                await ctx.channel.send('Desværre kammerat - du har tabt ' + str(n) + ' MichaelBucks.')

        except:
            await ctx.channel.send('Forkert indtastning.')

    @commands.command(brief = 'Check how many MichaelBucks you have in the bank.')
    async def bank(self, ctx):
        p = bank(str(ctx.author), self.df)
        await ctx.channel.send('Du har ' + str(p) + ' MichaelBucks til rådighed.')

    @commands.command(brief = 'Graph your MichaelBucks')
    async def graph(self, ctx):
        #Generates the graph based on the user.
         await ctx.channel.send('ja - god snak.')
    #    graph(str(ctx.author), self.df)
    #    asyncio.sleep(0.5)
    #    await ctx.channel.send(file=discord.File('./resources/other/temp.png'))

    @commands.command(brief = 'Send MichaelBucks to a friend')
    async def donate(self, ctx, amount : int, reciever : discord.Member):
        sender = ctx.author
        sender_str = str(ctx.author)
        reciever_str = str(reciever)
        if amount <= 0:
            await ctx.channel.send('Du kan ikke sende et negativt beløb.')
        else:
            self.df, rtrn = donate_points(sender_str, reciever_str, amount, self.df)
            if rtrn is True:
                await ctx.channel.send('Overførslen er gået igennem!')
            elif rtrn == -1:
                await ctx.channel.send('Så mange penge har du ikke, mester')
            elif rtrn == -2:
                await ctx.channel.send('Ukendt modtager.')
            else:
                print('Something else is wrong.')

    @commands.command(brief = 'Prints the highscore')
    async def highscore(self, ctx):
        s = highscore(self.df)
        await ctx.channel.send(s)

    @commands.command(brief = 'Removes the queue', hidden=True)
    async def rmqueue(self, ctx):
        clear_queue()

    @commands.command(aliases = ['play'], brief = 'Play a song from YouTube.')
    async def p(self, ctx, *args):
        #Plays the song.
        if len(args) == 1:
            args = args[0]
        else:
            args = ' '.join(args)
        if not song_available(args): await ctx.channel.send('Den skal lige downloades - der går lige to sekunder!')
        url, path = MBot_fetch_song(args)
        song = MBot_Audio(path)
        if self.channel != ctx.message.author.voice.channel:
            self.channel = ctx.message.author.voice.channel

        if self.vc is None:
            self.vc = await self.channel.connect()

        self.server = ctx.message.guild.voice_client

        if not self.vc.is_playing():
            song.play(self.vc)
            await ctx.channel.send('**Afspiller ' + url + '**')
        else:
            await ctx.channel.send('Vi hører lige musik, så ' + url + ' er sat i queue.')
            add_to_queue(path)

    @commands.command(brief='Skips the current song.')
    async def skip(self, ctx):
        if self.vc is not None:
            if self.vc.is_playing():
                self.vc.stop()

    @commands.command(brief='Play local song files. _mb pl list to get list of mp3s.')
    async def pl(self, ctx, *, arg):
        mp3s = load_mp3s()
        mp3 = str_to_mp3(arg, mp3s)
        if mp3 != '':
            file = MBot_Audio(mp3)

            if 'motoriske' in mp3: await ctx.channel.send(file=discord.File('./resources/gif/matrix.gif'))
            channel = ctx.message.author.voice.channel
            self.vc = await channel.connect()
            file.play(self.vc)
            while self.vc.is_playing():
                await asyncio.sleep(1)
            self.vc.stop()
            await ctx.voice_client.disconnect()
            self.vc = None
        elif arg.lower() == 'list':
        #Display the lists of mp3s to be played.
            s = list_mp3s()
            await ctx.channel.send(s)
        else:
            msg = custom_msg('unknown_mp3')
            await ctx.channel.send(msg)
  
    @tasks.loop(seconds=10)
    async def save(self):
        print('Points are saved')
        save_points(self.df)

    @tasks.loop(seconds=1)
    async def play_music(self):
        if self.vc is not None:
            if self.vc.is_playing():
                self.counter = 0
                self.pointcounter += 1
                if self.pointcounter == 5:
                    #Add points every 10 seconds.
                    self.df = add_points(self.df, self.channel.members)
                elif self.pointcounter == 10:
                    self.pointcounter = 0

            elif not is_queue_empty():
                #The bot is not playing and the queue is not empty. We should play the next song.
                path = fetch_from_queue()
                song = MBot_Audio(path)
                song.play(self.vc)
                remove_first_queue()

        if self.channel is not None:
            if self.vc is None:
                self.counter +=1
            elif not self.vc.is_playing():
                self.counter +=1
            if self.counter > 2: print('Michael leaves the channel in: ' + str(5-self.counter))

        if self.counter == 5:
            #The bot should disconnect from the channel after 10 seconds.
            await self.server.disconnect()
            self.vc = None
            self.channel = None
            self.counter = 0
            self.server = None

def setup(client):
    client.add_cog(Music(client))
