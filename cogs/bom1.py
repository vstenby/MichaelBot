import discord
from discord.ext import commands
from mbot_auxil import *
df_bom1 = load_bom1()

class Bom1(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Bom1'], brief = 'Access all of the Best of Mat 1 2018/2019 clips.',
    description = 'Access all of the Best of Mat 1 2018/2019 clips using this function.\n\nUsage:\n_mb bom1 list - Michael slides into your DMs with a list of all of the clips.\n_mb bom1 LX KY - sends you clip Y from lecture X.' )
    async def bom1(self, ctx, *, arg):
        if arg == 'list':
            str_list = msg_bom1_table(df_bom1)
            for str in str_list: await ctx.author.send(str)
        else:
            path = str_to_bom1(arg, df_bom1)
            if path == '':
                await ctx.channel.send('Den kan jeg desværre ikke finde.')
            else:
                try:
                    await ctx.channel.send(file=discord.File(path))
                except:
                    await ctx.channel.send('Desværre - den er for stor til Discord.')

def setup(client):
    client.add_cog(Bom1(client))
