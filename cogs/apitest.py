import discord
from discord.ext import commands
import requests
from io import StringIO
from mtranslate import translate

languages = {
    'polski': 'pl',
    'angielski': 'en',
    'niemiecki': 'de',
    'rosyjski': 'ru',
    'ruski': ' ru',
    'ukraiński': 'ua',
    'hiszpański': 'es',
    'francuski': 'fr',
    'włoski': 'it',
    'japoński': 'ja',
    'chiński': 'zh-CN',
    'czeski': 'cs',
    'portugalski': 'pt',
    'słowacki': 'sk',   
    'islandzki': 'is',
    'fiński': 'fi'
}

countries = {
    "AD": "Andora",
    "AE": "Zjednoczone Emiraty Arabskie",
    "AF": "Afganistan",
    "AG": "Antigua i Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AO": "Angola",
    "AQ": "Antarktyka",
    "AR": "Argentyna",
    "AS": "Samoa Amerykańskie",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AX": "Wyspy Alandzkie",
    "AZ": "Azerbejdżan",
    "BA": "Bośnia i Hercegowina",
    "BB": "Barbados",
    "BD": "Bangladesz",
    "BE": "Belgia",
    "BF": "Burkina Faso",
    "BG": "Bułgaria",
    "BH": "Bahrajn",
    "BI": "Burundi",
    "BJ": "Benin",
    "BL": "Saint-Barthélemy",
    "BM": "Bermudy",
    "BN": "Brunei Darussalam",
    "BO": "Boliwia",
    "BQ": "Bonaire, Sint Eustatius i Saba",
    "BR": "Brazylia",
    "BS": "Bahamy",
    "BT": "Bhutan",
    "BV": "Wyspa Bouveta",
    "BW": "Botswana",
    "BY": "Białoruś",
    "BZ": "Belize",
    "CA": "Kanada",
    "CC": "Wyspy Kokosowe",
    "CD": "Kongo (Demokratyczna Republika Konga)",
    "CF": "Republika Środkowoafrykańska",
    "CG": "Kongo",
    "CH": "Szwajcaria",
    "CI": "Wybrzeże Kości Słoniowej",
    "CK": "Wyspy Cooka",
    "CL": "Chile",
    "CM": "Kamerun",
    "CN": "Chiny",
    "CO": "Kolumbia",
    "CR": "Kostaryka",
    "CU": "Kuba",
    "CV": "Republika Zielonego Przylądka",
    "CW": "Curaçao",
    "CX": "Wyspa Bożego Narodzenia",
    "CY": "Cypr",
    "CZ": "Czechy",
    "DE": "Niemcy",
    "DJ": "Dżibuti",
    "DK": "Dania",
    "DM": "Dominika",
    "DO": "Republika Dominikańska",
    "DZ": "Algieria",
    "EC": "Ekwador",
    "EE": "Estonia",
    "EG": "Egipt",
    "EH": "Sahara Zachodnia",
    "ER": "Erytrea",
    "ES": "Hiszpania",
    "ET": "Etiopia",
    "FI": "Finlandia",
    "FJ": "Fidżi",
    "FK": "Falklandy (Malwiny)",
    "FM": "Mikronezja",
    "FO": "Wyspy Owcze",
    "FR": "Francja",
    "GA": "Gabon",
    "GB": "Wielka Brytania",
    "GD": "Grenada",
    "GE": "Gruzja",
    "GF": "Gujana Francuska",
    "GG": "Guernsey",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Grenlandia",
    "GM": "Gambia",
    "GN": "Gwinea",
    "GP": "Gwadelupa",
    "GQ": "Gwinea Równikowa",
    "GR": "Grecja",
    "GS": "Georgia Południowa i Sandwich Południowy",
    "GT": "Gwatemala",
    "GU": "Guam",
    "GW": "Gwinea Bissau",
    "GY": "Gujana",
    "HK": "Hongkong",
    "HM": "Wyspy Heard i McDonalda",
    "HN": "Honduras",
    "HR": "Chorwacja",
    "HT": "Haiti",
    "HU": "Węgry",
    "ID": "Indonezja",
    "IE": "Irlandia",
    "IS": "Islandia",
    "IN": "Indie",
    "ID": "Indonezja",
    "IQ": "Irak",
    "IR": "Iran",
    "IL": "Izrael",
    "JM": "Jamajka",
    "JP": "Japonia",
    "YE": "Jemen",
    "JE": "Jersey",
    "JO": "Jordania",
    "KY": "Kajmany",
    "KH": "Kambodża",
    "CM": "Kamerun",
    "CA": "Kanada",
    "QA": "Katar",
    "KZ": "Kazachstan",
    "KE": "Kenia",
    "KG": "Kirgistan",
    "KI": "Kiribati",
    "CO": "Kolumbia",
    "KM": "Komory",
    "CG": "Kongo",
    "KR": "Korea Południowa",
    "KP": "Korea Północna",
    "CR": "Kostaryka",
    "CU": "Kuba",
    "KW": "Kuwejt",
    "LA": "Laos",
    "LS": "Lesotho",
    "LB": "Liban",
    "LR": "Liberia",
    "LY": "Libia",
    "LI": "Liechtenstein",
    "LT": "Litwa",
    "LU": "Luksemburg",
    "LV": "Łotwa",
    "MK": "Macedonia Północna",
    "MG": "Madagaskar",
    "YT": "Majotta",
    "MO": "Makau S.A.R.",
    "MW": "Malawi",
    "MV": "Malediwy",
    "MY": "Malezja",
    "ML": "Mali",
    "MT": "Malta",
    "IM": "Wyspa Man",
    "MA": "Maroko",
    "MH": "Wyspy Marshalla",
    "MQ": "Martynika",
    "MU": "Mauritius",
    "MR": "Mauretania",
    "MX": "Meksyk",
    "FM": "Mikronezja",
    "MD": "Mołdawia",
    "MC": "Monako",
    "MN": "Mongolia",
    "MS": "Montserrat",
    "MZ": "Mozambik",
    "MM": "Mjanma (Birma)",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Holandia",
    "NO": "Norwegia",
    "NR": "Nauru",
    "NU": "Niue",
    "NZ": "Nowa Zelandia",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "Polinezja Francuska",
    "PG": "Papua-Nowa Gwinea",
    "PH": "Filipiny",
    "PK": "Pakistan",
    "PL": "Polska",
    "PM": "Saint-Pierre i Miquelon",
    "PN": "Pitcairn",
    "PR": "Portoryko",
    "PS": "Terytoria Palestyńskie",
    "PT": "Portugalia",
    "PW": "Palau",
    "PY": "Paragwaj",
    "QA": "Katar",
    "RE": "Reunion",
    "RO": "Rumunia",
    "RS": "Serbia",
    "RU": "Rosja",
    "RW": "Rwanda",
    "SA": "Arabia Saudyjska",
    "SB": "Wyspy Salomona",
    "SC": "Seszele",
    "SD": "Sudan",
    "SE": "Szwecja",
    "SG": "Singapur",
    "SH": "Wyspa Świętej Heleny",
    "SI": "Słowenia",
    "SJ": "Svalbard i Jan Mayen",
    "SK": "Słowacja",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Surinam",
    "SS": "Sudan Południowy",
    "ST": "Wyspy Świętego Tomasza i Książęca",
    "SV": "Salwador",
    "SX": "Sint Maarten (holenderska część)",
    "SY": "Syria",
    "SZ": "Eswatini",
    "TC": "Turks i Caicos",
    "TD": "Czad",
    "TF": "Francuskie Terytoria Południowe i Antarktyczne",
    "TG": "Togo",
    "TH": "Tajlandia",
    "TJ": "Tadżykistan",
    "TK": "Tokelau",
    "TL": "Timor Wschodni",
    "TM": "Turkmenistan",
    "TN": "Tunezja",
    "TO": "Tonga",
    "TR": "Turcja",
    "TT": "Trynidad i Tobago",
    "TV": "Tuvalu",
    "TW": "Tajwan",
    "TZ": "Tanzania",
    "UA": "Ukraina",
    "UG": "Uganda",
    "UM": "Dalekie Wyspy Mniejsze Stanów Zjednoczonych",
    "US": "Stany Zjednoczone",
    "UY": "Urugwaj",
    "UZ": "Uzbekistan",
    "VA": "Watykan",
    "VC": "Saint Vincent i Grenadyny",
    "VE": "Wenezuela",
    "VG": "Brytyjskie Wyspy Dziewicze",
    "VI": "Wyspy Dziewicze Stanów Zjednoczonych",
    "VN": "Wietnam",
    "VU": "Vanuatu",
    "WF": "Wallis i Futuna",
    "WS": "Samoa",
    "YE": "Jemen",
    "YT": "Majotta",
    "ZA": "Republika Południowej Afryki",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

class apitest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime', aliases = ['animedziewczynka', 'dziewczynka', 'an'])
    async def anime(self, ctx):
        response = requests.get("https://nekos.best/api/v2/neko")
        data = response.json()
        image = data["results"][0]["url"]
        await ctx.send(image)
    
    @commands.command(name='kawa', aliases = ['kawusia', 'kawka'])
    async def kawa(self, ctx):
        response = requests.get("https://coffee.alexflipnote.dev/random.json")
        data = response.json()
        kawa = data["file"]
        await ctx.send(kawa)
    
    @commands.command(name='lis', aliases = ['lisek'])
    async def lis(self, ctx):
        response = requests.get("https://randomfox.ca/floof/")
        data = response.json()
        image = data["image"]
        await ctx.send(image)
    
    @commands.command(name='rada', aliases=['porada'])
    async def rada(self, ctx):
        response = requests.get("https://api.adviceslip.com/advice")
        data = response.json()
        text = data["slip"]["advice"]
        translated = translate(text, 'pl', 'en')
        await ctx.send(text)
        await ctx.send(translated)
    
    @commands.command(name='plec', aliases=['płeć'])
    async def plec(self, ctx, arg):
        api = 'https://api.genderize.io/?name=' + str(arg)
        response = requests.get(api)
        data = response.json()
        plec = data["gender"]
        if plec == 'male':
            plec = 'mężczyzna'
        elif plec == 'female':
            plec = 'kobieta'
        else:
            plec = 'nie wiadomo'

        szansa = float(data["probability"])*100
        await ctx.send(f'Płeć imienia {arg}: {plec}\nPrawdopodobieństwo: {szansa:g}%')
        # await ctx.send(f'Prawdopodobieństwo: {szansa:g}%')
    
    @commands.command(name='obelga', aliases=['obraza'])
    async def obelga(self, ctx):
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        data = response.json()
        text = data["insult"]
        translated = translate(text, 'pl', 'en')
        await ctx.send(text)
        await ctx.send(translated)

    @commands.command(name='narodowosc', aliases=['narodowość', 'kraj'])
    async def narodowosc(self, ctx, arg):
        api = 'https://api.nationalize.io/?name=' + arg
        response = requests.get(api)
        data = response.json()
        dl = len(data['country'])
        for i in range(0, dl):
            kraj = data['country'][i]['country_id']
            if kraj in countries:
                kraj = countries[kraj]
            szansa = float(data['country'][i]['probability'])*100
            await ctx.send(f'Kraj, z którego pochodzi imię: {kraj}\nPrawdopodobieństwo: {szansa:g}%')

    @commands.command(name='wiek')
    async def wiek(self, ctx, arg):
        api = 'https://api.agify.io/?name=' + arg
        response = requests.get(api)
        data = response.json()
        text = data['age']
        await ctx.send(f'Przewidywany wiek podanego imienia: {text}')
            
    @commands.command(name='tekst', aliases = ['slowa', 'słowa'])
    async def tekst(self, ctx, *args):
        tytul = " ".join(args)
        # tytul = tytul.replace(' ', '+')
        api = 'https://api.popcat.xyz/lyrics?song=' + tytul
        response = requests.get(api)
        data = response.json()

        try:
            title = data["title"]
            lyrics = data["lyrics"]
            artist = data["artist"]
            await ctx.send(f'Tytuł: {title} - autor: {artist}')
            buffer = StringIO(lyrics)
            f = discord.File(buffer, filename="lyrics.txt")
            await ctx.send(file=f)
        except:
            await ctx.send('Nie jestem w stanie znaleźć słów do tej piosenki, spróbuj inaczej napisać tytuł')
    
    @commands.command(name='podryw', aliases = ['tekstnapodryw', 'napodryw'])
    async def podryw(self, ctx):
        response = requests.get('https://api.popcat.xyz/pickuplines')
        data = response.json()
        text = data['pickupline']
        translated = translate(text, 'pl', 'en')
        await ctx.send(text)
        await ctx.send(translated)
    
    @commands.command(name='auto', aliases = ['samochod', 'samochód'])
    async def auto(self, ctx):
        response = requests.get('https://api.popcat.xyz/car')
        data = response.json()
        image = data['image']
        # model = data['title']
        # await ctx.send(model)
        await ctx.send(image)
    
    @commands.command(name='ptak', aliases = ['ptaszek'])
    async def ptak(self, ctx):
        response = requests.get('https://some-random-api.ml/img/bird')
        data = response.json()
        image = data['link']
        await ctx.send(image)

    @commands.command(name='pies', aliases = ['piesek'])
    async def pies(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        image = data['message']
        await ctx.send(image)

    @commands.command(name='kot', aliases = ['kotek'])
    async def kot(self, ctx):
        response = requests.get('https://some-random-api.ml/img/cat')
        data = response.json()
        image = data['link']
        await ctx.send(image)

    @commands.command(name='kangur', aliases = ['kangurek'])
    async def kangur(self, ctx):
        response = requests.get('https://some-random-api.ml/img/kangaroo')
        data = response.json()
        image = data['link']
        await ctx.send(image)
    
    @commands.command(name='koala')
    async def koala(self, ctx):
        response = requests.get('https://some-random-api.ml/img/koala')
        data = response.json()
        image = data['link']
        await ctx.send(image)

    @commands.command(name='panda')
    async def panda(self, ctx):
        response = requests.get('https://some-random-api.ml/img/panda')
        data = response.json()
        image = data['link']
        await ctx.send(image)
    
    @commands.command(name='pikachu', aliases = ['pika'])
    async def pikachu(self, ctx):
        response = requests.get('https://some-random-api.ml/img/pikachu')
        data = response.json()
        image = data['link']
        await ctx.send(image)

    @commands.command(name='szop')
    async def szop(self, ctx):
        response = requests.get('https://some-random-api.ml/img/raccoon')
        data = response.json()
        image = data['link']
        await ctx.send(image)
    
    @commands.command(name='pandaruda', aliases = ['pandamala', 'pandamała', 'pandaczerwona'])
    async def pandaruda(self, ctx):
        response = requests.get('https://some-random-api.ml/img/red_panda')
        data = response.json()
        image = data['link']
        await ctx.send(image)
    
    @commands.command(name='wieloryb')
    async def wieloryb(self, ctx):
        response = requests.get('https://some-random-api.ml/img/whale')
        data = response.json()
        image = data['link']
        await ctx.send(image)
    
    @commands.command(name='kaczka', aliases = ['kaczuszka'])
    async def kaczka(self, ctx):
        response = requests.get('https://random-d.uk/api/v2/random')
        data = response.json()
        image = data['url']
        await ctx.send(image)
    
    @commands.command(name="shiba")
    async def shiba(self, ctx):
        response = requests.get('https://shibe.online/api/shibes')
        data = response.json()
        image = data[0]
        await ctx.send(image)

    @commands.command(name='cytat', aliases = ['cytatdnia'])
    async def cytat(self, ctx):
        response = requests.get('https://zenquotes.io/api/today')
        data = response.json()
        text = data[0]['q']
        translated = translate(text, 'pl', 'en')
        await ctx.send(text)
        await ctx.send(translated)
    
    @commands.command(name='tlumacz', aliases = ['tłumacz', 'tl'])
    async def tlumacz(self, ctx, *args):
        lang1 = args[0]
        lang2 = args[1]
        slowa = list(args)
        slowa.remove(lang1)
        slowa.remove(lang2)
        if lang1 in languages:
            lang1 = languages[lang1]
        
        if lang2 in languages:
            lang2 = languages[lang2]

        text = ' '.join(slowa)
        translated = translate(text, lang2, lang1)
        
        await ctx.send(translated)

async def setup(bot):
    await bot.add_cog(apitest(bot))