#Dependencies for the Game cog.
import discord
from discord.ext import commands
from functions import *
import emoji

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.game_ongoing = False
        self.answer = None

    @commands.command(brief='Start the grind for MichaelBucks.')
    async def game(self, ctx, *, arg):

        if len(arg.split(' ')) > 1:
            command = arg.split(' ')[0]
        else:
            command = arg

        if command.lower() == 'start':
            print('Game should be started')
            self.game_ongoing = True

        elif command.lower() == 'end':
            if self.game_ongoing:
                print('Game should be ended')
                self.game_ongoing = False
            else:
                print('No game at the moment')

        elif command.lower() == 'repeat':
            if self.game_ongoing:
                print('Sound should be repeated')
            else:
                print('No game at the moment')

        elif emoji.demojize(command) == ':OK_button:':
            if self.game_ongoing:
                print('Counted as a yes')
            else:
                print('No game at the moment')

        elif emoji.demojize(command) == ':cross_mark:':
            if self.game_ongoing:
                print('Counted as a no')
            else:
                print('No game at the moment')

        elif command.lower() == 'gamble':
            value = arg.split(' ')[1]
            try:
                value = int(value)
            except:
                print('Only integer rolls.')




def setup(client):
    client.add_cog(Game(client))
