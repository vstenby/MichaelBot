
@client.event
async def on_message(message):
    if message.content == 'Fortæl historien om Gauss':
        #Historien om Gauss skal fortælles.
        async with message.channel.typing():
            await message.channel.send('En endnu bedre historie som tager 1 minut at fortælle, det var hvad han gjorde som :four:-årig. Okay? Øhh - som :four:-årig gik han i skole sammen med resten af det gods han voksede op pås unger, og de havde selvfølgelig en privatlærer, fordi Gausses far var godsejer og meget velhavende. Okay? Og så skulle læreren drikke sin kaffe og læse sin avis eller et eller andet - han skulle ihvertfald have en pause, så han skulle finde på et eller andet at sætte de der unger til, så han sagde til dem: "Nu sætter I jer ned, nu lægger I alle tallene fra 1 til 100 sammen, og så sætter jeg mig og læser min avis." Og øjeblikkeligt rakte Gauss fingeren op og sagde: "Det bliver 5050". Og jeg ved ikke, om Gauss blev slået hårdt i hovedet eller fik hældt kaffen ud over sig eller sådan et eller andet, det kunne man jo nok godt forestille sig, ikke også? Læreren var fuldstændig målløs og sagde: "Hvad gjorde du?" "Jo, det er jo nemt nok. Fordi 1 plus 100, det er 101, 2 plus 99, det er 101, det kan jeg gøre 50 gange. 50 gange 101, det er 5050. Hvor svært kan det være?"')

    if message.content == 'Kan du se det Michael?':
        await message.channel.send('Ja, jeg kan godt se det...')


        await client.process_commands(message)
        if message.content == 'Er det fredag i dag?':
            today = datetime.datetime.today().weekday()
            if today == 4:
                await message.channel.send('Hold kæft - det er det sgu kraftedenme! Det er jo sådan en dag man skal have varme harboe på bænken med drengene!')
            else:
                await message.channel.send('Desværre ikke.')
        elif message.content == 'Fortæl historien om Gauss':
            #Historien om Gauss skal fortælles.
            async with message.channel.typing():
                await message.channel.send('En endnu bedre historie som tager 1 minut at fortælle, det var hvad han gjorde som :four:-årig. Okay? Øhh - som :four:-årig gik han i skole sammen med resten af det gods han voksede op pås unger, og de havde selvfølgelig en privatlærer, fordi Gausses far var godsejer og meget velhavende. Okay? Og så skulle læreren drikke sin kaffe og læse sin avis eller et eller andet - han skulle ihvertfald have en pause, så han skulle finde på et eller andet at sætte de der unger til, så han sagde til dem: "Nu sætter I jer ned, nu lægger I alle tallene fra 1 til 100 sammen, og så sætter jeg mig og læser min avis." Og øjeblikkeligt rakte Gauss fingeren op og sagde: "Det bliver 5050". Og jeg ved ikke, om Gauss blev slået hårdt i hovedet eller fik hældt kaffen ud over sig eller sådan et eller andet, det kunne man jo nok godt forestille sig, ikke også? Læreren var fuldstændig målløs og sagde: "Hvad gjorde du?" "Jo, det er jo nemt nok. Fordi 1 plus 100, det er 101, 2 plus 99, det er 101, det kan jeg gøre 50 gange. 50 gange 101, det er 5050. Hvor svært kan det være?"')
        elif message.content == 'Hvilket skema er det bedste?':
            await message.channel.send('Skema B, naturligvis.')
        elif message.content == 'Kan vi høre en banger?':
            await message.channel.send('Jeg sætter altså ikke "Vektor kom" på...')
        elif message.content.lower() == 'hvordan ganger man matricer?':
            await message.channel.send(file=discord.File('./resources/gif/matrix.gif'))
@client.event
async def on_message(message):
    await client.process_commands(message)
    q, a = load_QA()
    answ = QA(message.content, q, a)
    if answ != '':
        await message.channel.send(answ)

######################



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
            'cachedir': False,
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

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

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
