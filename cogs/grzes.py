import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import random
import time

class grzes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stop_counting = False
        self.lie_count = 0
        self.load_lie_count()
    
    def load_lie_count(self):
        try:
            with open('./smieci/licznik_klamstw.txt', 'r') as f:
                self.lie_count = int(f.read())
        except FileNotFoundError:
            pass

    def save_lie_count(self):
        with open('./smieci/licznik_klamstw.txt', 'w') as f:
            f.write(str(self.lie_count))

    @commands.command(name = 'grzes', aliases = ['grzegorz', 'Grzes', 'Grzegorz', 'gregoros12pl', 'Grześ', 'grześ', 'gregoros12', 'gregoros', 'kasztan'])
    async def grzes(self, ctx):
        los = random.randint(0,1)
        
        if los == 0:
            with open('./smieci/odpowiedzi.txt', 'r') as f:
                losowa_odpowiedz = f.readlines()
                odpowiedz = random.choice(losowa_odpowiedz)
            await ctx.send('Grzes to ' + odpowiedz)
        else:
            with open('./smieci/odpowiedzi2.txt', 'r') as f:
                losowa_odpowiedz2 = f.readlines()
                odpowiedz2 = random.choice(losowa_odpowiedz2)
            await ctx.send('Grzes to ' + odpowiedz2)
        
    @commands.command(name = 'losuj', aliases = ['los', 'random', 'rand'])
    async def losuj(self, ctx, arg):
        liczby = arg
        liczby = int(liczby)
        a = list(range(1, int(liczby+1)))
        random.shuffle(a)

        if liczby % 2 == 0:
            for x in range(0, int(liczby/2)):
                b = random.choice(a)
                a.remove(b)
                b2 = random.choice(a)
                a.remove(b2)

                await ctx.send(f'```{x+1}. {b} - {b2}```')
        else:
            await ctx.send('Jest nieparzyście, więc Grześ będzie grał solo')
            liczby = int(liczby-1)
            for x in range(0, int(liczby/2)):
                b = random.choice(a)
                a.remove(b)
                b2 = random.choice(a)
                a.remove(b2)

                await ctx.send(f'```{x+1}. {b} - {b2}```')
            await ctx.send(f'```{int(liczby/2+1)}. {a[0]} - 😭```')

    @commands.command(name='zart', aliases=['żart','kawal','kawał'])
    async def zart(self, ctx):
        los = random.randint(0, 20)
        with open('./smieci/zarty.txt', 'r') as f:
            losowy_zart = f.readlines()
            zart = losowy_zart[los]

        with open('./smieci/odpnazarty.txt', 'r') as f:
            losowa_odpnazart = f.readlines()
            odpnazart = losowa_odpnazart[los]

        await ctx.send(zart)
        time.sleep(4)
        await ctx.send(odpnazart)

    @commands.command(name='grzespochwala', aliases=['grzesmilo', 'grzesdobry', 'grześpochwała', 'grześpochwala', 'grzespochwała', 'grześmiło', 'grześmilo'])
    async def grzespochwala(self, ctx):
        await ctx.send('Bot myśli...')
        time.sleep(2)
        await ctx.send('...')
        time.sleep(2)
        await ctx.send('Dobre słowa o Grzesiu: brak')

    @commands.command(name='poll', aliases = ['ankieta'])
    async def poll(self, ctx, *args):
        numbers = ["1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
        
        text = list(args)
        text = ' '.join(args)
        podzial = text.split('/')
        pytanie = podzial[0]

        podzial.remove(pytanie)

        ile = int(len(podzial))

        if ile > 10:
            await ctx.send('Za dużo opcji, można maksymalnie 10')
        else:
            embed_message = discord.Embed(title=pytanie, color=discord.Color.random())
            embed_message.set_author(name=f"Stworzył: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            for i in range (0, ile):
                embed_message.add_field(name=f"Opcja {numbers[i]}", value=podzial[i], inline=True)
            
            embed_message.set_footer(text="Grajek by anteczek")            
            
            message = await ctx.send(embed=embed_message)
            for i in range(0, ile):
                await message.add_reaction(f'{numbers[i]}')
    
    @commands.command(name='kabarecik', aliases = ['Kabarecik', 'Anteczek', 'anteczek'])
    async def kabarecik(self, ctx):
        los = random.randint(0,1)
        await ctx.send('Prawdziwa twarz anteczka:')
        if los == 0:
            await ctx.send(file=discord.File("./smieci/chad1.png"))
        else:
            await ctx.send(file=discord.File("./smieci/chad2.png"))
    
    @commands.command(name='mydlo', aliases = ['mydło', 'Mydlo', 'Mydło'])
    async def mydlo(self, ctx):
        await ctx.send('Prawdziwa forma mydła:')
        await ctx.send(file=discord.File("./smieci/mydlo.jpg"))
    
    @commands.command(name='kepa', aliases = ['kepski', 'kępski', 'kiepski', 'kempa', 'kępa', 'kęmpa'])
    async def kepa(self, ctx):
        await ctx.send('Prawdziwe oblicze kępy:')
        await ctx.send(file=discord.File("./smieci/lech.jpg"))
    
    @commands.command(name='stachu', aliases = ['stasiek'])
    async def stachu(self, ctx):
        los = random.randint(0,1)
        await ctx.send('Stachu ultimate form:')
        if los == 0:
            await ctx.send(file=discord.File("./smieci/uberchad.jpg"))
        else:
            await ctx.send(file=discord.File("./smieci/pudzian.jpg"))
    
    @commands.command(name='rabarbar')
    async def rabarbar(self, ctx):
        await ctx.send('Warzywna wersja grzesia:')
        await ctx.send(file=discord.File("./smieci/rabarbar.jpg"))
    
    @commands.command(name='julek', aliases = ['juleczek'])
    async def julek(self, ctx):
        await ctx.send('Magiczna forma julka:')
        await ctx.send(file=discord.File("./smieci/potter.jpg"))

    @commands.command(name='mateusz', aliases = ['rudy'])
    async def mateusz(self, ctx):
        await ctx.send('Czarna wersja mateusza:')
        await ctx.send(file=discord.File("./smieci/pirat.png"))

    @commands.command(name='marcinek', aliases = ['marcin'])
    async def marcinek(self, ctx):
        await ctx.send('13-letni marcin o krok od zdobycia mistrzostwa Mokotowa w szachach:')
        await ctx.send(file=discord.File("./smieci/carlsen.jpg"))

    @commands.command(name='grzesklamca', aliases = ['grzeswymowka', 'grześkłamca', 'grzeskłamca', 'grześklamca', 'grześwymówka', 'grzeswymówka', 'grześwymowka'])
    async def grzesklamca(self, ctx):
        with open('./smieci/wymowki.txt', 'r') as f:
            losowa_wymowka = f.readlines()
            wymowka = random.choice(losowa_wymowka)
        await ctx.send(wymowka)
    
    @app_commands.command(name='ping', description='Latency cos tam test')
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.") 

    @commands.command(name='simp')
    async def simp(self, ctx, arg):
        ile = int(arg)*60
        count = 0
        message = await ctx.send(f"Liczę od {count} sekund...")
        first_minute_elapsed = False
        while count < ile and not self.stop_counting:
            await asyncio.sleep(1)
            count += 1
            if count >= 60:
                if not first_minute_elapsed:
                    first_minute_elapsed = True
                    minutes = count // 60
                    seconds = count % 60
                    await message.edit(content=f"Liczę od {minutes} minut{'y' if minutes < 2 else ''} i {seconds} sekund...")
                else:
                    minutes = count // 60
                    seconds = count % 60
                    await message.edit(content=f"Liczę od {minutes} minut{'y' if minutes < 2 else ''} i {seconds} sekund...")
            else:
                await message.edit(content=f"Liczę od {count} sekund...")
        if self.stop_counting:
            await ctx.send(content="Liczenie zostało zatrzymane")
        else:
            await message.edit(content=f"Czas minął")
            licznik = 0
            #moje 370962411202674689
            #kempa 434025592627789827
            user_id = '434025592627789827'
            user = await self.bot.fetch_user(user_id)
            while licznik < 7:
                await asyncio.sleep(5)
                licznik+=1
                await ctx.send(user.mention)

    @commands.command()
    async def stopsimp(self, ctx):
        if self.stop_counting == False:
            self.stop_counting = True   
        else:
            self.stop_counting = False
    
    @commands.command(name='klamca', aliases  = ['kłamca'])
    async def klamca(self, ctx):
        self.lie_count += 1
        await ctx.send(f"Grześ skłamał po raz {self.lie_count}")
        self.save_lie_count()

async def setup(bot):
    await bot.add_cog(grzes(bot))