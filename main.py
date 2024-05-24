import asyncio
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

with open('token.txt', 'r') as f:
    token = f.readline()

client = discord.Client(intents=intents)

test = '1068536914275221534'
drugi = '535526406805913601'

bot = commands.Bot(command_prefix='.', intents=intents, activity = discord.Game(name="rabarbar [.help]"), default_guild_ids = test)
    
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    #v sprawdza na ilu serverach jest bot
    # print(f'{len(bot.guilds)}')

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
        
async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())