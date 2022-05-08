import os
import disnake
from disnake.ext import commands

import logging
from dotenv import load_dotenv
load_dotenv()



# https://docs.python.org/3/library/logging.html#module-logging

logger = logging.getLogger('disnake')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

loggercmd = logging.getLogger("disnakecommands")
loggercmd.setLevel(logging.INFO)
handlercmd = logging.FileHandler(filename='disnakecommands.log', encoding='utf-8', mode='w+')
handlercmd.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
loggercmd.addHandler(handlercmd)


loggercmd = logging.getLogger("disnakecommands.main")
bot = commands.InteractionBot(sync_commands_debug=True,owner_id=int(os.environ["BUCKYID"]),test_guilds=[851204839605927946],intents=disnake.Intents.all(),reload=True)
# bot = commands.Bot(test_guilds=[771385874688245770,])
# bot = commands.InteractionBot(test_guilds=[771385874688245770,851204839605927946],sync_commands_debug=True,)

@bot.event
async def on_ready():
    loggercmd.debug(f"'{bot.user.name}#{bot.user.discriminator}' is ready!")



@bot.slash_command()
async def ping(inter:disnake.CmdInter):
    if not await bot.is_owner(inter.author):
        inter.send("Oh, you're not Bucky")
        return
    await inter.send(f"Pong!\n```{bot.latency}```")



devcogs = [
    "debug",
    "dev"
]
for cog in devcogs:
    bot.load_extension(f"devcogs.{cog}",)

disabled = [
    # "fun.py",
    # "weather.py"
    # "download.py"
] 
for cog in os.listdir("cogs"):
    if os.path.isfile(f"cogs/{cog}") and cog not in disabled: 
        bot.load_extension(f"cogs.{cog.split('.')[0]}",)
print("running")
bot.run(os.environ["DISBOTTOKEN1"])
