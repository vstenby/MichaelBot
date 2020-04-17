import discord
from discord.ext import commands
import time
import datetime
import pandas as pd
import numpy as np
import os
import random
import asyncio
import youtube_dl

#client = commands.Bot(command_prefix = 'Michael')
client = commands.Bot(command_prefix = 'mbot ')

@client.event
async def on_ready():
    print('MichaelBot er klar til at køre!')
    await client.change_presence(activity=discord.Game(name="Gauss-Elimination"))

@client.command(pass_context=True)
async def join(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@client.command(aliases=['ses'],pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def gauss(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('gauss.mp3'), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    vc.stop()
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def lofi(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('lofi.mp3'), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    vc.stop()
    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def eNote(ctx, arg):
    enotes = pd.read_html('./files/enotes.html')[0]['Name']
    url = 'https://01005.compute.dtu.dk/enotes/' + enotes[:].astype(str)
    arg = int(arg)
    return_url = url[arg-1]
    embed = discord.Embed(
        title = 'Forfatter: Karsten Schmidt',
        color = discord.Colour.blue()
    )

    enotestr = 'eNote ' + str(arg)
    embed.add_field(name=enotestr, value=return_url)

    await ctx.channel.send('Var der nogen der spurgte om eNote ' + str(arg) + '?')
    await ctx.channel.send(embed=embed)

@client.command(pass_context=True)
async def Mat1Guessr(ctx):
    await ctx.channel.send('To sekunder - så får du lige et klip!')
    num = random.randint(1, 4)
    filepath = './Mat1Guessr/mat1guessr' + str(num) + '.mp4'
    await ctx.channel.send(file=discord.File(filepath))
    await ctx.channel.send('Klippet er fra nedenstående forelæsning:')
    df = pd.read_excel('./Mat1Guessr/correct_answers.xlsx')
    answer = str(df['Tekst'].loc[df['Nummer']==num].iloc[0])
    await ctx.channel.send('|| ' + answer + ' ||')

@client.command(pass_context=True)
async def drukspil(ctx):
    embed = discord.Embed(
        title = 'Mat1-drukspillet',
        description = 'Udarbejdet og testet udførligt af:\nViktor Stenby (s174483) og Rasmus Aagaard (s164419)\n\n',
        colour = discord.Colour.blue()
    )

    green = 'Hvis I regner med at kunne holde til mere end én Matematik 1-forelæsning, råder vi til at holde jer til disse basic-regler, som fungerer som drukspillets bread and butter.\n\n'
    embed.add_field(name='**"Det er sgu da nemt nok, jeg taster det ind på min lommeregner."**', value=green, inline=False)

    green_rules = '"Kan I se det?"\n\n"Er I med på den?"\n\n"Nå! Øøøh..." eller "Nå! Okay..." efter en joke.\n\nMichael underspiller Mat 1 / pointerer at det faktisk ikke er svært.\n\nHyggedag.\n\nMichael nævner øl og/eller bodega.\n\nMichael siger, at man er havnet på en øde ø.\n\nBINGO/OK i stedet for QED.\n\n\nMichael referer til DTU som et eliteuniversitet.\n\nMichael nævner, at det jo er fredag.\n\n\nMichael knækker kridtet.'
    embed.add_field(name='**De grønne regler**', value=green_rules, inline=True)
    embed.add_field(name='Antal tårer', value='1 tår\n\n1 tår\n\n2 tårer\n\n\n2 tårer\n\n\n3 tårer\n\n3 tårer\n\n3 tårer\n\n\n4 tårer **eller** bund hvis de gamle grækere bliver nævnt.\n\n5 tårer\n\n\nFællesskål og dobbelt op, hvis drukspillet spilles på en fredag.\n\n6 tårer **eller** bund hvis han efterfølgende bander.', inline=True)

    yellow = 'Hvis man ikke føler, at det går stærkt nok med "Kan I se det" i sig selv, og man gerne vil spice sit drukspil yderligere op, så er dette nogle gode additions til regelsættet.\n\n'
    embed.add_field(name='**"I kan godt se, at det bliver sjovere og sjovere, ik?"**', value=yellow, inline=False)

    yellow_rules = 'Michael nævner Maple\n\n"Læg lige mærke til..."\n\n"Hvordan var det nu... Nåååh, jo!"\n\n"Jamen, lad os se engang..."\n\n"Kigge hårdt på..."\n\n"Fidusen er ..."\n\nMichael sætter "2 streger" under facit uden at løfte kridtet.\n\nMichael laver lyde med munden.\n\nMichael fortæller anekdoten om da Gauss lagde tallene 1 til 100 sammen.'
    embed.add_field(name='**De gule regler**', value=yellow_rules, inline=True)
    embed.add_field(name='Antal tårer', value='1 tår\n\n2 tårer\n\n2 tårer\n\n2 tårer\n\n2 tårer\n\n3 tårer\n\n3 tårer\n\n\n3 tårer\n\nKnap en ny øl op og tøm den mens du lytter til historien.')

    red = "Hvis man ikke føler, at man har regler nok i forvejen og har brug for at save sig selv fuldstændig i stykker til Matematik 1 forelæsninger, så er her nogle flere forslag til regler, der vil sætte gang i festen."
    red_rules = 'Den gange den\n\nMichael nævner fisk og/eller bitter\n\n"Den her forelæsning ville Maple kunne holde på ...", "I Maple ville dette tage..." eller tilsvarende'
    embed.add_field(name='**"Så nu skal I simpelthen bare være vågne allesammen, ellers går det durk til helvede det her."**', value=red, inline=False)
    embed.add_field(name='**De røde regler**', value=red_rules, inline=True)
    embed.add_field(name='Antal tårer', value='2 tårer\n\n1 shots Fisk og/eller 2 shots bitter\n\nDu har den tid til at bunde din øl', inline=True)
    embed.set_footer(text='Vi skal gøre jer opmærksomme på, at spillet er lavet af kærlighed til Michael og til kurset. Lad altså være med at dukke op til Mat1 forelæsningerne og spille drukspillet, da det forstyrrer de andre der prøver at følge med. Sæt jer ihvertfald i det mindste i Auditorie 43 i stedet for, hvis det endelig er.')
    await ctx.channel.send(embed=embed)

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content == 'Er det fredag i dag?':
        today = datetime.datetime.today().weekday()
        if today == 4:
            await message.channel.send('Hold kæft - det er det sgu kraftedenme! Det er jo sådan en dag man skal have varme harboe på bænken med drengene!')
        else:
            await message.channel.send('Desværre ikke.')
    elif message.content == 'Kan I se det?':
        await message.channel.send(file=discord.File('./files/sedet.mp4'))
    elif message.content == 'Fortæl historien om Gauss':
        #Historien om Gauss skal fortælles.
        async with message.channel.typing():
            await message.channel.send('En endnu bedre historie som tager 1 minut at fortælle, det var hvad han gjorde som :four:-årig. Okay? Øhh - som :four:-årig gik han i skole sammen med resten af det gods han voksede op pås unger, og de havde selvfølgelig en privatlærer, fordi Gausses far var godsejer og meget velhavende. Okay? Og så skulle læreren drikke sin kaffe og læse sin avis eller et eller andet - han skulle ihvertfald have en pause, så han skulle finde på et eller andet at sætte de der unger til, så han sagde til dem: "Nu sætter I jer ned, nu lægger I alle tallene fra 1 til 100 sammen, og så sætter jeg mig og læser min avis." Og øjeblikkeligt rakte Gauss fingeren op og sagde: "Det bliver 5050". Og jeg ved ikke, om Gauss blev slået hårdt i hovedet eller fik hældt kaffen ud over sig eller sådan et eller andet, det kunne man jo nok godt forestille sig, ikke også? Læreren var fuldstændig målløs og sagde: "Hvad gjorde du?" "Jo, det er jo nemt nok. Fordi 1 plus 100, det er 101, 2 plus 99, det er 101, det kan jeg gøre 50 gange. 50 gange 101, det er 5050. Hvor svært kan det være?"')
    elif message.content == 'Hvordan Gauss-eliminerer man?':
        await message.channel.send(file=discord.File('./files/gauss_elimination.gif'))
    elif message.content == 'Hvilket skema er det bedste?':
        await message.channel.send('Skema B, naturligvis.')

client.run('NzAwNjQ1MDI3OTUyNDU5ODA3.XpmJ8w.YDnmXXd9bYuB1bNF3_54_taQNHc')
