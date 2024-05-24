import discord
from discord.ext import commands
# import youtube_dl
import yt_dlp
from youtube_search import YoutubeSearch
import time
import random
import datetime
import asyncio

def convert(seconds):
  seconds = seconds % (24 * 3600)
  seconds %= 3600
  minutes = seconds // 60
  seconds %= 60
    
  return "%02d:%02d" % (minutes, seconds)

def convert2(seconds):
  seconds = seconds % (24 * 3600)
  hour = seconds // 3600
  seconds %= 3600
  minutes = seconds // 60
  seconds %= 60
    
  return "%d:%02d:%02d" % (hour, minutes, seconds)

class music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.is_playing = False
    self.is_paused = False
    # [formatted_url, voice_channel, clear_url, given_text]
    self.music_queue = []
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    # Voice channel it is connected to
    self.vc = None
    self.perm = False
    # self.last_active_time = datetime.datetime.now()
    # self.activity_checker_task = self.bot.loop.create_task(self.check_activity())
    # self.is_looping = False

  # async def check_activity(self):
  #   while True:
  #     # check if the bot has been inactive for 5 minutes
  #     if (datetime.datetime.now() - self.last_active_time).total_seconds() > 300:
  #         await self.vc.disconnect() # disconnect from the channel
  #         return
  #     await asyncio.sleep(300) # check every minute / zmieniłem na 5 minut

  # @commands.Cog.listener()
  # async def on_message(self, message):
  #   # reset the timer on each message
  #   self.last_active_time = datetime.datetime.now()
    # your message handling code goes here

  # @commands.Cog.listener()
  # async def on_voice_state_update(self, member, before, after):
  #   # reset the timer on each voice state update
  #   if member == self.bot.user and before.channel != after.channel:
  #       self.last_active_time = datetime.datetime.now()

  # def cog_unload(self):
  #   self.activity_checker_task.cancel()

  def search_yt(self, text):
    # First we check if the given text is not a link
    if text.find("www.youtube.com") == -1:
      try:
        result = YoutubeSearch(text, max_results=1).to_dict()
        return("http://www.youtube.com" + result[0].get("url_suffix"))
      except:
        return "EMPTY"
    return text
  
  def play_next(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      url = self.music_queue[0][0]
      self.current_song = self.music_queue[0][2]
      # self.current_songurl = self.music_queue[0]

      self.music_queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
      
    else:
      self.is_playing = False

  #not a discord command but infinite check
  async def play_music(self, ctx):
    if len(self.music_queue) > 0:
      self.is_playing = True

      url = self.music_queue[0][0]

      if self.vc is None or not self.vc.is_connected():
        # Reconnect if the bot is not connected
        voice_channel = self.music_queue[0][1]
        self.vc = await voice_channel.connect()
      
      # Move to the correct voice channel
      await self.vc.move_to(self.music_queue[0][1])

      self.current_song = self.music_queue[0][2]
      # self.current_songurl = self.music_queue[0]
      self.music_queue.pop(0)
      
      self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

    else:
      self.is_playing = False
      
  @commands.command(name = "play", aliases = ["p", 'graj', 'g'])
  async def play (self, ctx, *args):
    text = " ".join(args)
    
    try:
      voice_channel = ctx.author.voice.channel
      if self.is_paused:
        self.vc.resume()
      else:
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
          url = self.search_yt(text)
          # We need to check if there was a match with the given text
          if url == "EMPTY":
            await ctx.send("Nie mogę otworzyć tego filmiku, spróbuj ponownie")
          elif url.startswith('https://www.youtube.com/playlist'):
            info = ydl.extract_info(url, download=False)
            duration = 0
            for i in info['entries']:
              #do youtube-dl
              # url2 = i['formats'][0]['url']   
              #do yt-dlp
              url2 = i['url']
              duration += i['duration']
              self.music_queue.append([url2, voice_channel, url, text])
              if not self.is_playing:
                await self.play_music(ctx)

            thumbnailURL = info['thumbnails'][3]['url']
            title = info['title']
            embed_message = discord.Embed(title=title, color=discord.Color.random())
            embed_message.set_author(name=f"Dodał: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            if duration/3600 >= 1:
              duration = convert2(duration)
            else:
              duration = convert(duration)
            # embed_message.add_field(name='Playlista', value=f"link: {url}", inline=False)
            embed_message.add_field(name=f"Czas trwania: {duration}", value=f"link: {url}", inline=False)
            embed_message.set_footer(text="Grajek by anteczek")            
            embed_message.set_thumbnail(url=f"{thumbnailURL}")
            # file = discord.File("./smieci/nutka.png", filename="image.png")
            # embed_message.set_thumbnail(url='attachment://image.png')

            await ctx.send(embed=embed_message)
          else:
            info = ydl.extract_info(url, download=False)
            #do youtube-dl
            # url2 = info['formats'][0]['url']
            #do yt-dlp
            url2 = info['url']
            self.music_queue.append([url2, voice_channel, url, text])

            title = info['title']
            thumbnailURL = info['thumbnail']
            duration = info['duration']

            if duration/3600 >= 1:
              duration = convert2(duration)
            else:
              duration = convert(duration)

            embed_message = discord.Embed(title=title, color=discord.Color.random())
            embed_message.set_author(name=f"Dodał: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            embed_message.add_field(name=f"Czas trwania: {duration}", value=f"link: {url}", inline=False)
            embed_message.set_footer(text="Grajek by anteczek")            
            embed_message.set_thumbnail(url=f"{thumbnailURL}")

            await ctx.send(embed=embed_message)

            if not self.is_playing:
              await self.play_music(ctx)
            # else:
            #   await ctx.send(url + " Added to the list :musical_note:")
    except:
      await ctx.send("Nie jesteś na kanale głosowym debilu dzbanie grzesiu")

  @commands.command(name = "forceplay", aliases = ["forcep", 'fp', 'fplay'])
  async def forceplay (self, ctx, *args):
    text = " ".join(args)

    try:
      voice_channel = ctx.author.voice.channel
      if self.is_paused:
        self.vc.resume()
      else:
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
          url = self.search_yt(text)
          # We need to check if there was a match with the given text
          if url == "EMPTY":
            await ctx.send("Nie mogę otworzyć tego filmiku, spróbuj ponownie")
          elif url.startswith('https://www.youtube.com/playlist'):
            info = ydl.extract_info(url, download=False)
            duration = 0
            for i in info['entries']:
              #do youtube-dl
              # url2 = i['formats'][0]['url']   
              #do yt-dlp
              url2 = i['url']
              duration += i['duration']
              # self.music_queue.append([url2, voice_channel, url, text])
              self.music_queue.insert(0, [url2, voice_channel, url, text])
              if not self.is_playing:
                await self.play_music(ctx)

            thumbnailURL = info['thumbnails'][3]['url']
            title = info['title']
            embed_message = discord.Embed(title=title, color=discord.Color.random())
            embed_message.set_author(name=f"Dodał: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            # embed_message.add_field(name='Playlista', value=f"link: {url}", inline=False)
            if duration/3600 >= 1:
              duration = convert2(duration)
            else:
              duration = convert(duration)
            embed_message.add_field(name=f"Czas trwania: {duration}", value=f"link: {url}", inline=False)
            embed_message.set_footer(text="Grajek by anteczek")
            embed_message.set_thumbnail(url=f"{thumbnailURL}")      
            # file = discord.File("./smieci/nutka.png", filename="image.png")
            # embed_message.set_thumbnail(url='attachment://image.png')

            await ctx.send(embed=embed_message)
            # if self.vc != None and self.vc:
            #   self.vc.stop()
            #   await self.play_music(ctx)
            if self.vc is not None and self.vc.is_playing():
              self.vc.stop()

          else:
            info = ydl.extract_info(url, download=False)
            #do youtube-dl
            # url2 = info['formats'][0]['url']
            #do yt-dlp
            url2 = info['url']
            # self.music_queue.append([url2, voice_channel, url, text])
            self.music_queue.insert(0, [url2, voice_channel, url, text])
            title = info['title']
            thumbnailURL = info['thumbnail']
            duration = info['duration']
            if duration/3600 >= 1:
              duration = convert2(duration)
            else:
              duration = convert(duration)

            embed_message = discord.Embed(title=title, color=discord.Color.random())
            embed_message.set_author(name=f"Dodał: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            embed_message.add_field(name=f"Czas trwania: {duration}", value=f"link: {url}", inline=False)
            embed_message.set_footer(text="Grajek by anteczek")            
            embed_message.set_thumbnail(url=f"{thumbnailURL}")

            await ctx.send(embed=embed_message)

            if not self.is_playing:
              await self.play_music(ctx)

            # if self.vc != None and self.vc:
            #   self.vc.stop()
            #   await self.play_music(ctx)
            if self.vc is not None and self.vc.is_playing():
              self.vc.stop()
            # else:
            #   await ctx.send(url + " Added to the list :musical_note:")
    except:
      await ctx.send("Nie jesteś na kanale głosowym debilu dzbanie grzesiu")

  @commands.command(name="pause", aliases=['stop', 'zatrzymaj'])
  async def pause(self, ctx, *args):
    if self.is_playing:
      self.is_playing = False
      self.is_paused = True
      self.vc.pause()
      await ctx.send("Bot zatrzymany")
    elif self.is_paused:
      self.vc.resume()
      await ctx.send("Bot wznowiony")

  @commands.command(name = "resume", aliases=["r", 'dalej', 'wznow'])
  async def resume(self, ctx, *args):
    if self.is_paused:
      self.vc.resume()
      await ctx.send("Bot wznowiony")

  @commands.command(name="skip", aliases=["s", 'pomin'])
  async def skip(self, ctx):
    # if self.vc != None and self.vc:
    #   await ctx.send("Piosenka została pominięta :arrow_right:")
    #   self.vc.stop()
    #   await self.play_music(ctx)
    if self.vc is not None and self.vc.is_playing():
      await ctx.send("Piosenka została pominięta :arrow_right:")
      self.vc.stop()

  @commands.command(name="queue", aliases=["q", 'kolejka', 'kol'])
  async def queue(self, ctx):
    retval = ""
    for i in range(0, len(self.music_queue)):
      retval += str(i+1) + ".  " + self.music_queue[i][3] + "\n"

    if retval != "":
      await ctx.send("Piosenki w kolejce: \n" + retval)
    else:
      await ctx.send("Kolejka jest pusta. :pensive:")

  @commands.command(name="clear", aliases=["c", "bin", 'czysc', 'kosz'])
  async def clear(self, ctx):
    if self.vc is not None and self.is_playing:
      self.vc.stop()
    self.music_queue = []
    await ctx.send("Kolejka jest wyczyszczona. :shower:")

  @commands.command(name="leave", aliases=["disconnect", "l", "d", 'exit'])
  async def dc(self, ctx):
    # await ctx.send("Naura :cowboy:")
    # self.is_playing = False
    # self.is_paused = False
    # await self.vc.disconnect()
    if self.vc is not None and self.vc.is_connected():
      await ctx.send("Naura :cowboy:")
      self.is_playing = False
      self.is_paused = False
      self.music_queue = []  # Clear the queue
      self.vc.stop()  # Stop playing music
      await self.vc.disconnect()

  @commands.command(name="remove", aliases = ['delete', 'del'])
  async def remove(self, ctx, arg):
    try:
      nr = int(arg)-1
      if self.is_playing:
        if len(self.music_queue) >= nr+1:
          self.music_queue.pop(nr)
          await ctx.send(f'Został usunięty {arg} numer z kolejki')
        else:
          await ctx.send('Na tej pozycji nie ma żadnego numeru')
      else:
        await ctx.send('Najpierw bot musi puszczać muzykę')
    except:
      await ctx.send('Coś poszło nie tak')

  # @commands.command(name = 'loop', aliases=['petla', 'lp', 'pt'])
  # async def loop(self, ctx):
  #   if self.is_looping:
  #     self.is_looping = False
  #     await ctx.send("Looping is now **disabled**")
  #   else:
  #     self.is_looping = True
  #     await ctx.send("Looping is now **enabled**")

  #     while self.is_looping and self.is_playing:
  #       self.music_queue.insert(0, self.current_songurl)
  #       await asyncio.sleep(80)

  @commands.command(name = 'loop', aliases=['petla', 'lp', 'pt'])
  async def loop(self, ctx, arg):
    try:
      ile = int(arg)
      if ile > 0 and ile < 15:
        await ctx.send(f'Dodano {ile}-krotnie ostatnią piosenkę z kolejki')
        last = self.music_queue[len(self.music_queue)-1]
        while ile > 0:
          self.music_queue.append(last)
          ile-=1
      else:
        await ctx.send('Nie mozna tyle razy dodac piosenki')
    except:
      await ctx.send('Coś poszło nie tak')

  @commands.command(name = 'add', aliases = ['dodaj'])
  async def add(self, ctx, *args):
    try:
      nr = int(args[0])-1
      ile = int(args[1])
      if ile > 0 and ile < 15:
        await ctx.send(f'Dodano {ile}-krotnie {nr+1} piosenkę z kolejki')
        numer = self.music_queue[nr]
        while ile > 0:
          self.music_queue.append(numer)
          ile-=1
      else:
        await ctx.send('Nie mozna tyle razy dodac piosenki')
    except:
      await ctx.send('Coś poszło nie tak')

  @commands.command(name = 'dokonca', aliases = ['dokońca', 'Dokońca'])
  async def dokonca(self, ctx):
    text = 'ZBUKU - Do końca'
    try:
      voice_channel = ctx.author.voice.channel
      if self.is_paused:
        self.vc.resume()
      else:
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
          url = 'https://www.youtube.com/watch?v=jd_p2eAd3xc'
          # We need to check if there was a match with the given text
          if url == "EMPTY":
            await ctx.send("Nie mogę otworzyć tego filmiku, spróbuj ponownie")
          else:
            info = ydl.extract_info(url, download=False)
            #do youtube-dl
            # url2 = info['formats'][0]['url']
            #do yt-dlp
            url2 = info['url']
            # self.music_queue.append([url2, voice_channel, url, text])
            if len(self.music_queue) == 0:
              self.music_queue.append([url2, voice_channel, url, text])
            else:
              self.music_queue.insert(0, [url2, voice_channel, url, text])
            title = info['title']
            thumbnailURL = info['thumbnail']
            duration = info['duration']
            duration = convert(duration)

            embed_message = discord.Embed(title=title, color=discord.Color.random())
            embed_message.set_author(name=f"Dodał: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            embed_message.add_field(name=f"Czas trwania: {duration}", value=f"link: {url}", inline=False)
            embed_message.set_footer(text="Grajek by anteczek")            
            embed_message.set_thumbnail(url=f"{thumbnailURL}")

            await ctx.send(embed=embed_message)

            if not self.is_playing:
              await self.play_music(ctx)

            # if self.vc != None and self.vc:
            #   self.vc.stop()
            #   await self.play_music(ctx)
            if len(self.music_queue) != 0:
              if self.vc is not None and self.vc.is_playing():
                self.vc.stop()
            # else:
            #   await ctx.send(url + " Added to the list :musical_note:")
    except:
        await ctx.send("Nie jesteś na kanale głosowym debilu dzbanie grzesiu")   

  @commands.command(name = 'wiesia', aliases = ['jasper', 'wiesiaolol', 'wiesiaołoł'])
  async def wiesia(self, ctx):
    text = 'dawid jasper - wiesia oł oł'
    try:
      voice_channel = ctx.author.voice.channel
      if self.is_paused:
        self.vc.resume()
      else:
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
          url = 'https://www.youtube.com/watch?v=C8NGR1TI7D4'
          # We need to check if there was a match with the given text
          if url == "EMPTY":
            await ctx.send("Nie mogę otworzyć tego filmiku, spróbuj ponownie")
          else:
            info = ydl.extract_info(url, download=False)
            #do youtube-dl
            # url2 = info['formats'][0]['url']
            #do yt-dlp
            url2 = info['url']
            # self.music_queue.append([url2, voice_channel, url, text])
            if len(self.music_queue) == 0:
              self.music_queue.append([url2, voice_channel, url, text])
            else:
              self.music_queue.insert(0, [url2, voice_channel, url, text])
            title = info['title']
            thumbnailURL = info['thumbnail']
            duration = info['duration']
            duration = convert(duration)

            embed_message = discord.Embed(title=title, color=discord.Color.random())
            embed_message.set_author(name=f"Dodał: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            embed_message.add_field(name=f"Czas trwania: {duration}", value=f"link: {url}", inline=False)
            embed_message.set_footer(text="Grajek by anteczek")            
            embed_message.set_thumbnail(url=f"{thumbnailURL}")

            await ctx.send(embed=embed_message)

            if not self.is_playing:
              await self.play_music(ctx)

            # if self.vc != None and self.vc:
            #   self.vc.stop()
            #   await self.play_music(ctx)
            if len(self.music_queue) != 0:
              if self.vc is not None and self.vc.is_playing():
                self.vc.stop()
            # else:
            #   await ctx.send(url + " Added to the list :musical_note:")
    except:
        await ctx.send("Nie jesteś na kanale głosowym debilu dzbanie grzesiu")  
        
  @commands.command(name = 'shuffle', aliases = ['szufla', 'tasuj', 'mieszaj'])
  async def shuffle(self, ctx):
    random.shuffle(self.music_queue)
    await ctx.send('Kolejka została pomieszana losowo')

  @commands.command(name = 'currentsong', aliases = ['teraz', 'now', 'current'])
  async def currentsong(self, ctx):
    try:
      await ctx.send(f'Teraz leci: {self.current_song}')
    except:
      await ctx.send('Nie leci aktualnie żadna piosenka')

  @commands.command(name = 'permission', aliases = ['poz', 'pozwolenie', 'per'])
  async def permission(self, ctx):
    if self.perm == True:
      self.perm = False
    else:
      self.perm = True
    await ctx.send(f'Glos w komendzie .kadzidlo: {self.perm}')

  @commands.command(name = 'kadzidlo', aliases = ['kadz', 'grzeskadzidlo', 'kadzidło', 'Kadzidło', 'Kadzidlo'])
  async def kadzidlo(self, ctx):
    text = 'kadzidło'
    if self.perm == True:
      try:
        voice_channel = ctx.author.voice.channel
        if self.is_paused:
          self.vc.resume()
        else:
          with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            url = 'https://www.youtube.com/watch?v=br-XXVWWhqU'
            # We need to check if there was a match with the given text
            if url == "EMPTY":
              await ctx.send("Nie mogę otworzyć tego filmiku, spróbuj ponownie")
            else:
              info = ydl.extract_info(url, download=False)
              #do youtube-dl
              # url2 = info['formats'][0]['url']
              #do yt-dlp
              url2 = info['url']
              # self.music_queue.append([url2, voice_channel, url, text])
              if len(self.music_queue) > 0:
                self.music_queue.insert(0, [url2, voice_channel, url, text])
              else:
                self.music_queue.append([url2, voice_channel, url, text])

              if not self.is_playing:
                await self.play_music(ctx)
              
              if len(self.music_queue) > 0:
                # if self.vc != None and self.vc:
                #   self.vc.stop()
                #   await self.play_music(ctx)
                if self.vc is not None and self.vc.is_playing():
                  self.vc.stop()
              # else:
              #   await ctx.send(url + " Added to the list :musical_note:")
      except:
          if not self.is_playing:
            await ctx.send("Nie jesteś na kanale głosowym debilu dzbanie grzesiu")

    await ctx.send(file=discord.File('./smieci/kadzidlo.png'))
    time.sleep(4)
    await ctx.send('Grzesiu przyszykuj kadzidło')
    time.sleep(4)
    await ctx.send('Kadzidło przyszykuj')

  @commands.command(name='playlist', aliases = ['playlisty', 'plist', 'pl'])
  async def playlist(self, ctx):
    await ctx.send(file=discord.File("./smieci/playlisty.txt"))

async def setup(bot):
    await bot.add_cog(music(bot))