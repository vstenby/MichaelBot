import discord
from discord.ext import commands, tasks
import asyncio
import numpy as np
import os
import sqlite3
import pandas as pd


def start_wallet():
    conn = sqlite3.connect('wallet.db')
    cmd = """ CREATE TABLE IF NOT EXISTS wallet (
                                id integer PRIMARY KEY,
                                mbucks integer DEFAULT 0
                                ); """
    c = conn.cursor()
    c.execute(cmd)
    return conn, c


def update_wallet(id, dmbucks, cursor):
    #Add points to ID
    cmd = """ INSERT INTO wallet(id, mbucks) VALUES(?,?)
                     ON CONFLICT(id) DO UPDATE SET mbucks = mbucks + ?;"""
    cursor.execute(cmd, (id,dmbucks,dmbucks))
    return

def read_wallet(id, cursor):
    cmd = "SELECT mbucks FROM wallet WHERE id = ?;"
    t = cursor.execute(cmd, (id,)).fetchone()
    if t is None:
        return 0
    else:
        return t[0]
    
def gamble(id, amount, cursor):
    if amount == "all":
        amount = read_wallet(id, cursor)
    else:
        try:
            amount = int(amount)
        except:
            amount = None
            return -4, amount
    
    wallet = read_wallet(id, cursor)
    
    if amount > wallet:
        #Too big of a gamble
        return -1, amount
    
    if amount == 0:
        #You can't gamble 0 mbucks
        return -2, amount
    
    if amount < 0:
        #You can't gamble negative mbucks.
        return -3, amount
    
    if np.random.randint(0,2):
        update_wallet(id, amount, cursor)
        return 1, amount
    else:
        update_wallet(id, -amount, cursor)
        return 0, amount

def donate(giver, reciever, amount, cursor):
    if amount == "all":
        amount = read_wallet(giver, cursor)
    else:
        try:
            amount = int(amount)
        except:
            return
    
    wallet = read_wallet(giver, cursor)
    
    if amount > wallet:
        #Too big of a donation
        return -1
    if amount == 0:
        #You can't donate 0 mbucks.
        return -2
    if amount < 0:
        #You can't donate negative mbucks
        return -3
    if giver == reciever:
        #You can't donate to yourself
        return -4
    
    #Otherwise, let the transaction go through.
    update_wallet(giver, -amount, cursor)
    update_wallet(reciever, amount, cursor)
    return 1

def topn(n, cursor):
    return cursor.execute('SELECT id, mbucks FROM wallet ORDER BY mbucks DESC LIMIT ?;',(n,)).fetchall()

def print_df(connection):
    df = pd.read_sql_query("SELECT * FROM wallet", connection)

class GambleCog(commands.Cog):
    """GambleCog"""
    
    def __init__(self, bot):
        self.bot = bot
        self.conn, self.cursor = start_wallet()
        self.givepoints.start()

    @commands.command(name='wup')
    async def _wup(self, ctx):
        """ Test function 2 """
        print(pd.read_sql_query("SELECT * FROM wallet", self.conn))
        #df = print_df(self.conn)
        #print(df)
        
    @commands.command(name='gamble')
    async def _gamble(self, ctx, *, arg):
        argin = ctx.message.content.replace('_mb gamble ','').lower()
        rtrn, val = gamble(ctx.message.author.id, argin, self.cursor)
        if rtrn == 0:
            await ctx.message.channel.send(f'Desværre {ctx.message.author.mention}, du har tabt {val} MichaelBucks.')
        elif rtrn == 1:
            await ctx.message.channel.send(f'Tillykke {ctx.message.author.mention}, du har vundet {val} MichaelBucks.')
        else:
            await ctx.message.channel.send('Fejlbeskrivelse mangler, men du har nok været en klovn.')        
            
    @commands.command(name='bank')
    async def _bank(self, ctx):
        """ Prints how much you have """
        val = read_wallet(ctx.message.author.id, self.cursor)
        await ctx.message.channel.send(f'{ctx.message.author.mention}, du har {val} MichaelBucks.')
    
    @commands.command(name='donate')
    async def _donate(self, ctx, amount : int, user : discord.User):
        """ Donates to a person """
        
        rtrn = donate(ctx.message.author.id, user.id, amount, self.cursor)
        
        if rtrn == -1:
            await ctx.message.channel.send(f'{ctx.message.author.mention}, du kan ikke sende så mange MichaelBucks.')
        elif rtrn == -2:
            await ctx.message.channel.send(f'{ctx.message.author.mention}, du kan ikke sende 0 MichaelBucks.')
        elif rtrn == -3:
            await ctx.message.channel.send(f'{ctx.message.author.mention}, du kan ikke sende et negativt antal MichaelBucks.')
        elif rtrn == -4:
            await ctx.message.channel.send(f'{ctx.message.author.mention}, du kan ikke sende til dig selv.')
        elif rtrn == 1:
            await ctx.message.channel.send(f'{ctx.message.author.mention}, du har sendt {amount} MichaelBucks til {user.mention}')
        else:
            await ctx.message.channel.send('Et eller andet gik galt.')
                      
                      
    @commands.command(name='highscore')
    async def _highscore(self, ctx):
        """ Prints the highscore """
        top5 = topn(5, self.cursor)
        s = "```\n"
        s = s + 'MichaelBucks - highscore\n\n'
        for id, mbuck in top5:
            name = self.bot.get_user(id).name
            s += f'{name} med {mbuck} MichaelBucks.\n'
        s = s + '\n```'
        await ctx.message.channel.send(s)
        
    @tasks.loop(seconds=5)
    async def givepoints(self):
        print('Giving points!')
        #Leaves automatically if Michael is not saying anything.
        ids = []; names = [];
        for guild in self.bot.guilds:
            for member in guild.members:
                id = member.id
                name = member.name
                if member.status == discord.Status.online and not member.bot:
                    ids.append(id)
                    names.append(name)
        
        ids = np.unique(ids)
        for id in ids: update_wallet(int(id), 1, self.cursor)


def setup(bot):
    bot.add_cog(GambleCog(bot))

