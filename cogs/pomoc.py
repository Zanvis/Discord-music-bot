from io import StringIO
import discord
from discord.ext import commands

class pomoc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases = ['h', 'pomoc', 'komendy'])
    async def help(self, ctx):
        komendy = """
Poszczególne komendy:
.help / .pomoc / .h / .komendy - wyświetla wszystkie dostępne komendy
.tylkokomendy / .komendykategoria - wyświetla same kategoria komend
.komendymuzyka / .komendymuzyczne - wyświetla tylko komendy muzyczne
.komendygrzes / .komendygrześ - wyświetla tylko komendy o grzesiu
.komendydiscord / .komendydiscordowe - wyświetla tylko komendy około-discordowe
.komendyfunkcyjne / .komendyfunkcja - wyśwetla tylko komendy funkcyjne
.komendyrekreacyjne / .komendyfun - wyświetla tylko komendy rekreayjne

Komendy muzyczne:
.play / .graj / .p / .g - puszcza muzykę, link/słowa klucze, bez playlist
.pause / .stop / .zatrzymaj - zatrzymuje muzykę
.resume / .dalej / .wznow / .r - wznawia muzykę
.skip / .pomin / .s - pomija aktualnie lecącą piosenkę
.queue / .q / .kolejka / .kol - wyświetla kolejkę
.clear / .bin / .kosz / .czysc / .c - czyści kolejkę
.leave / .exit / .disconnect / .l / .d - wyrzuca bota
.shuffle / .szufla / .tasuj / .mieszaj - przestawia losowo piosenki w kolejce
.forceplay / .fp / .forcep / .fplay - natchmiast puszcza daną piosenkę
.remove [nr] / .delete [nr] /.del [nr] - usuwa daną piosenkę z kolejki
.loop [ile] / .petla [ile] / .lp [ile] / .pt [ile] - dodaje [ile]-krotnie ostatnią piosenkę z kolejki
.add [nr] [ile] / .dodaj [nr] [ile] - dodaje do kolejki [nr] piosenkę z kolejki [ile]-krotnie
.currentsong / .teraz / .now / .current - pokazuje jaka obecnie leci piosenka
.dokonca / .dokońca - natychmiast puszcza ZBUKU - Do końca
.wiesia / .jasper / .wiesiaolol / .wiesiaołoł - natychmiast puszcza dawid jasper - wiesia oł oł
.playlist / .playlisty / .plist - pokazuje dostępne w bazie playlisty, by nie było trzeba ich googlować

Komendy o grzesiu:
.grzes - mówi prawdę o grzesiu
.grzespochwala / .grzesmilo / .grzesdobry - pisze miło o grzesiu
.kadzidlo - sprawdz
.pozwolenie / .poz - pozwolenie na dźwięk komendy .kadzidlo
.kłamca / .klamca - wyświetla ile razy Grzesiu skłamał (licznik nie resetuje się po wyłączeniu bota)
.grzesklamca / grzeswymowka - wyświetla jakąś wymówkę grzesia

Komendy około-discordowe
.kabarecik / .anteczek - pokazuje prawdziwą twarz anteczka
.mydlo - prawdziwa forma mydła
.kepa / .kempa / .kepski / .kiepski - pokazuje prawdziwe oblicze kępy
.stachu / .stasiek - ostateczna forma staska
.rabarbar - rabarbar (ciekawe o kogo chodzi)
.julek / .juleczek - magiczna forma julka
.mateusz / .rudy - czarna wersja mateusza
.marcin / .marcinek - mistrzowska wersja marcina

Komendy funkcyjne:
.losuj [liczba osob] /.los [liczba osob] - losuje pary w zależności od liczby osób
.ankieta [pytanie] / [pierwsza opcja] / [druga opcja] / ... - tworzy ankietę na zadane pytanie z podanymi dostępnymi opcjami

Komendy rekreacyjne:
.simp [liczba minut] - zaczyna odliczać wyznaczony czas, a po skończeniu odliczania oznacza kempe pare razy
.stopsimp - zatrzymuje liczenie
.zart / .żart - opowiada żart (uwaga, są mocne)
.anime / .dziewczynka / .animedziewczynka / .an - wyświetla anime dziewczynkę
.kawa / .kawusia / .kawka - wyświetla kawę
.lis / .lisek - wyświetla lisa
.rada / .porada - wyświetla poradę (po angielsku i z tłumaczeniem na polski)
.plec [imię] / .płeć [imię] - wyświetla płeć imienia oraz jego prawdopodobieństwo
.obelga / .obraza - wyświetla dość zaawansowaną obelgę (po angielsku i z tłumaczeniem na polski)
.kraj [imię] / .narodowosc [imię] / .narodowość [imię] - wyświetla możliwe kraje pochodzenia imienia oraz ich prawdopodobieństwo
.wiek [imię] - wyświetla prawdopodobny wiek imienia
.tekst [tytuł] / .slowa [tytuł] / .słowa [tytuł] - wyświetla tekst do danej piosenki (działa dość pokracznie - wiele piosenek może nie zadziałać)
.podryw / .napodryw / .tekstnapodryw - wyświetla tekst na podryw (po angielsku i z tłumaczeniem na polski)
.auto / .samochod / .samochód - wyświetla samochód
.ptak / .ptaszek - wyświetla ptaka (zwierzę takie jakby co)
.pies / .piesek - wyświetla psa
.kot / .kotek - wyświetla kota
.kangur / .kanguerk - wyświetla kangura
.koala - wyświetla koalę
.panda - wyświetla pandę
.pikachu / .pika - wyświetla pikachu
.szop - wyświetla szopa
.pandaruda / .pandamala / .pandamała / .pandaczerwona - wyświetla pandę rudą
.wieloryb - wyświetla wieloryba
.kaczka / .kaczuszka - wyświetla kaczkę
.shiba - wyświetla psa rasy shiba
.tlumacz [tekst po polsku] / .tłumacz [tekst po polsku] / .tl [tekst po polsku] - tłumaczenie tekstu z polskiego na angielski
"""
        buffer = StringIO(komendy)
        f = discord.File(buffer, filename="komendy.txt")
        await ctx.send(file=f)

    @commands.command(name='tylkokomendy', aliases = ['komendykategoria'])
    async def tylkokomendy(self, ctx):
        await ctx.send("""
```
Poszczególne komendy:
.help / .pomoc / .h / .komendy - wyświetla wszystkie dostępne komendy
.tylkokomendy / .komendykategoria - wyświetla same kategoria komend
.komendymuzyka / .komendymuzyczne - wyświetla tylko komendy muzyczne
.komendygrzes / .komendygrześ - wyświetla tylko komendy o grzesiu
.komendydiscord / .komendydiscordowe - wyświetla tylko komendy około-discordowe
.komendyfunkcyjne / .komendyfunkcja - wyśwetla tylko komendy funkcyjne
.komendyrekreacyjne / .komendyfun - wyświetla tylko komendy rekreayjne
```
""")

    @commands.command(name='komendymuzyka', aliases = ['komendymuzyczne'])
    async def komendymuzyka(self, ctx):
        await ctx.send("""
```
Komendy muzyczne:
.play / .graj / .p / .g - puszcza muzykę, link/słowa klucze, bez playlist
.pause / .stop / .zatrzymaj - zatrzymuje muzykę
.resume / .dalej / .wznow / .r - wznawia muzykę
.skip / .pomin / .s - pomija aktualnie lecącą piosenkę
.queue / .q / .kolejka / .kol - wyświetla kolejkę
.clear / .bin / .kosz / .czysc / .c - czyści kolejkę
.leave / .exit / .disconnect / .l / .d - wyrzuca bota
.shuffle / .szufla / .tasuj / .mieszaj - przestawia losowo piosenki w kolejce
.forceplay / .fp / .forcep / .fplay - natchmiast puszcza daną piosenkę
.remove [nr] / .delete [nr] /.del [nr] - usuwa daną piosenkę z kolejki
.loop [ile] / .petla [ile] / .lp [ile] / .pt [ile] - dodaje [ile]-krotnie ostatnią piosenkę z kolejki
.add [nr] [ile] / .dodaj [nr] [ile] - dodaje do kolejki [nr] piosenkę z kolejki [ile]-krotnie
.currentsong / .teraz / .now / .current - pokazuje jaka obecnie leci piosenka
.dokonca / .dokońca - natychmiast puszcza ZBUKU - Do końca
.wiesia / .jasper / .wiesiaolol / .wiesiaołoł - natychmiast puszcza dawid jasper - wiesia oł oł
.playlist / .playlisty / .plist - pokazuje dostępne w bazie playlisty, by nie było trzeba ich googlować
```
""")

    @commands.command(name='komendygrzes', aliases = ['komendygrześ'])
    async def komendygrzes (self, ctx):
        await ctx.send("""
```
Komendy o grzesiu:
.grzes - mówi prawdę o grzesiu
.grzespochwala / .grzesmilo / .grzesdobry - pisze miło o grzesiu
.kadzidlo - sprawdz
.pozwolenie / .poz - pozwolenie na dźwięk komendy .kadzidlo
.kłamca / .klamca - wyświetla ile razy Grzesiu skłamał (licznik nie resetuje się po wyłączeniu bota)
.grzesklamca / grzeswymowka - wyświetla jakąś wymówkę grzesia
```
""")

    @commands.command(name='komendydiscord', aliases = ['komendydiscordowe'])
    async def komendydiscord(self, ctx):
        await ctx.send("""
```
Komendy około-discordowe
.kabarecik / .anteczek - pokazuje prawdziwą twarz anteczka
.mydlo - prawdziwa forma mydła
.kepa / .kempa / .kepski / .kiepski - pokazuje prawdziwe oblicze kępy
.stachu / .stasiek - ostateczna forma staska
.rabarbar - rabarbar (ciekawe o kogo chodzi)
.julek / .juleczek - magiczna forma julka
.mateusz / .rudy - czarna wersja mateusza
.marcin / .marcinek - mistrzowska wersja marcina
```
""")

    @commands.command(name='komendyfunkcyjne', aliases = ['komendyfunkcja'])
    async def komendyfunkcyjne(self, ctx):
        await ctx.send("""
```
Komendy funkcyjne:
.losuj [liczba osob] /.los [liczba osob] - losuje pary w zależności od liczby osób
.ankieta [pytanie] / [pierwsza opcja] / [druga opcja] / ... - tworzy ankietę na zadane pytanie z podanymi dostępnymi opcjami
```
""")

    @commands.command(name='komendyrekreacyjne', aliases = ['komendyfun'])
    async def komendyrekreacyjne(self, ctx):
        await ctx.send("""
```
Komendy rekreacyjne:
.simp [liczba minut] - zaczyna odliczać wyznaczony czas, a po skończeniu odliczania oznacza kempe pare razy
.stopsimp - zatrzymuje liczenie
.zart / .żart - opowiada żart (uwaga, są mocne)
.anime / .dziewczynka / .animedziewczynka / .an - wyświetla anime dziewczynkę
.kawa / .kawusia / .kawka - wyświetla kawę
.lis / .lisek - wyświetla lisa
.rada / .porada - wyświetla poradę (po angielsku i z tłumaczeniem na polski)
.plec [imię] / .płeć [imię] - wyświetla płeć imienia oraz jego prawdopodobieństwo
.obelga / .obraza - wyświetla dość zaawansowaną obelgę (po angielsku i z tłumaczeniem na polski)
.kraj [imię] / .narodowosc [imię] / .narodowość [imię] - wyświetla możliwe kraje pochodzenia imienia oraz ich prawdopodobieństwo
.wiek [imię] - wyświetla prawdopodobny wiek imienia
.tekst [tytuł] / .slowa [tytuł] / .słowa [tytuł] - wyświetla tekst do danej piosenki (działa dość pokracznie - wiele piosenek może nie zadziałać)
.podryw / .napodryw / .tekstnapodryw - wyświetla tekst na podryw (po angielsku i z tłumaczeniem na polski)
.auto / .samochod / .samochód - wyświetla samochód
.ptak / .ptaszek - wyświetla ptaka (zwierzę takie jakby co)
.pies / .piesek - wyświetla psa
.kot / .kotek - wyświetla kota
.kangur / .kanguerk - wyświetla kangura
.koala - wyświetla koalę
.panda - wyświetla pandę
.pikachu / .pika - wyświetla pikachu
.szop - wyświetla szopa
.pandaruda / .pandamala / .pandamała / .pandaczerwona - wyświetla pandę rudą
.wieloryb - wyświetla wieloryba
.kaczka / .kaczuszka - wyświetla kaczkę
.shiba - wyświetla psa rasy shiba
.tl [tekst po polsku] - tłumaczenie tekstu z polskiego na angielski
```
""")

async def setup(bot):
    await bot.add_cog(pomoc(bot))