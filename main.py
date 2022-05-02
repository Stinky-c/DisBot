from datetime import datetime
import discord
import os
import requests as req
import json
from dotenv import load_dotenv
load_dotenv() # only loads in the same dir

# bot = discord.Bot(debug_guilds=[771385874688245770,],intents=discord.Intents.all())
bot = discord.Bot(debug_guilds=[771385874688245770,851204839605927946],intents=discord.Intents.all())
# bot = discord.Bot(debug_guilds=[771385874688245770,851204839605927946])

'''
Big words that i cant spell
ephemeral
description

people i guess:     851204839605927946
storage:            771385874688245770
'''

@bot.event
async def on_ready():
    # bot.add_view(View())
    print(f"{bot.user}; {datetime.now()}")

# @bot.event
# async def on_message_delete(message):
    # await message.channel.send(message.content)


devcogs = [
    "debug",
    # "dev"
]
for cog in devcogs:
    bot.load_extension(f"devcogs.{cog}",)
    print(f"devcogs.{cog} loaded ")

disabled = [
    # "fun.py",
    "weather.py"
] 
for cog in os.listdir("cogs"):
    if not os.path.isdir(f"cogs/{cog}") and cog not in disabled: 
        bot.load_extension(f"cogs.{cog.split('.')[0]}",)
        print(f"cogs.{cog.split('.')[0]} loaded ")


bot.run(os.environ["DISBOTTOKEN1"])
# bot.run(os.environ["DISBOTTOKEN3"])