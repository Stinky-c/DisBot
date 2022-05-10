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
handlercmd = logging.FileHandler(filename='disnakecommands.log', encoding='utf-8', mode='a+')
handlercmd.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
loggercmd.addHandler(handlercmd)


loggercmd = logging.getLogger("disnakecommands.main")
bot = commands.InteractionBot(sync_commands_debug=True,owner_id=int(os.environ["BUCKYID"]),test_guilds=[851204839605927946,771385874688245770],intents=disnake.Intents.all())
# bot = commands.InteractionBot(owner_id=int(os.environ["BUCKYID"]),intents=disnake.Intents.all(),sync_commands=True)

@bot.event
async def on_ready():
    loggercmd.debug(f"'{bot.user.name}#{bot.user.discriminator}' is ready!")


devcogs = [
    "debug",
    "dev",
    "market"
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
