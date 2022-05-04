import os
import disnake
from disnake.ext import commands

import logging
# logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
load_dotenv()



# https://docs.python.org/3/library/logging.html#module-logging
import disnake

logger = logging.getLogger('disnake')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



# bot = commands.Bot(sync_commands_debug=True)
# bot = commands.Bot(test_guilds=[771385874688245770,])
bot = commands.InteractionBot(test_guilds=[771385874688245770,851204839605927946],sync_commands_debug=True,)

@bot.event
async def on_ready():
    print("The bot is ready!")



@bot.slash_command()
async def ping(inter:disnake.CmdInter):
    print(inter)
    await inter.response.send_message("hello")



devcogs = [
    "debug",
    "dev"
]
for cog in devcogs:
    bot.load_extension(f"devcogs.{cog}",)
    print(f"devcogs.{cog} loaded ")

disabled = [
    "fun.py",
    "weather.py"
] 
for cog in os.listdir("cogs"):
    if not os.path.isdir(f"cogs/{cog}") and cog not in disabled: 
        bot.load_extension(f"cogs.{cog.split('.')[0]}",)
        print(f"cogs.{cog.split('.')[0]} loaded ")

bot.run(os.environ["DISBOTTOKEN1"])