#Dependencies for the Response cog
import discord
from discord.ext import commands
import random
import pandas as pd
from functions import *

class Response(commands.Cog):

    def __init__(self, client):
        self.client = client
    #Commands
    @commands.command(brief='Links to an eNote', description='Michael helps you out by linking to your requested eNote.\nUsage: _mb eNote <number>')
    async def eNote(self, ctx, arg):
        enotes = pd.read_html('./resources/other/enotes.html')[0]['Name']
        url = 'https://01005.compute.dtu.dk/enotes/' + enotes[:].astype(str)
        if int(arg) > 29 or int(arg) < 1:
            await ctx.channel.send('Den eNote har vi vist ikke...')
        else:
            arg = int(arg)-1
            enote_name = enotes[arg]
            enote_name = enote_name.replace('_', ' ')
            enote_name = enote_name.replace('ae', 'æ')
            enote_name = enote_name.replace('oe', 'ø')
            enote_name = enote_name.replace('aa', 'å')
            return_url = url[arg]
            embed = discord.Embed(
                title = 'eNote ' + enote_name,
                color = discord.Colour.blue()
            )
            enotestr = 'Forfatter: Karsten Schmidt'
            embed.add_field(name=enotestr, value=return_url)
            eNote_response = enote_comment(arg)
            await ctx.channel.send(eNote_response)
            await ctx.channel.send(embed=embed)


    #Drukspil-kommandoen.
    @commands.command(aliases=['Drukspil', 'drukspil'], brief='Posts the official Mat 1 drukspil ruleset.')
    async def Mat1Drukspillet(self, ctx):
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

    #Events
    @commands.Cog.listener()
    async def on_message(self, message):
        q, a = load_QA()
        answ = QA(message.content, q, a)
        if answ != '':
            await message.channel.send(answ)
        if message.content.lower() == 'hvad skal jeg spørge om, michaelbot?':
            q_random = random.choice(q)
            if len(q_random) > 1: q_random = random.choice(q)
            q_random = q_random[0]
            await message.channel.send('"' + q_random + '" kunne da være et godt spørgsmål.')

def setup(client):
    client.add_cog(Response(client))
