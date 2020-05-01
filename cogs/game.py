#Dependencies for the Game cog.
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
from functions import *
import asyncio
import random

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

class Game(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.music = self.client.get_cog('Music')
        self.pointdf = load_points()

        #Start the tasks adding the points
        self.points.start()

    @commands.command(brief='MichaelBot rolls a die.')
    async def roll(self, ctx, n : int):
        r = random.randint(1, n)
        await ctx.channel.send('Det blev en ' + str(r) +"'er.")

    @commands.command(brief = 'Gamble your hard earned MichaelBucks')
    async def gamble(self, ctx, arg):

        if arg == 'all': arg = bank(str(ctx.author), self.pointdf)

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

            self.df, val = gamble(str(ctx.author), self.pointdf, n)
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
        graph(str(ctx.author), self.df)
        asyncio.sleep(0.5)
        await ctx.channel.send(file=discord.File('./resources/other/temp.png'))

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



    @tasks.loop(seconds=10)
    async def points(self):
        #Add points every 5 seconds.
        try:
            if self.music.vc.is_playing():
                #Then we should add the points
                self.pointdf = add_points(self.pointdf, self.music.channel.members)
        except:
            print('Bot is not playing, and no points should be added.')

        #The points are saved once every 10 seconds.
        save_points(self.pointdf)





def setup(client):
    client.add_cog(Game(client))
