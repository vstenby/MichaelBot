
@client.event
async def on_ready():
    print('MichaelBot is online!')
    await client.change_presence(activity=discord.Game(name="Gauss-Elimination"))

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
