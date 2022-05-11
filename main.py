import os
import disnake
from disnake.ext import commands
import anyconfig

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

tml = anyconfig.load("./config.toml")

bot = commands.InteractionBot(
    sync_commands_debug=True,
    owner_ids=tml["id"]["ownerids"],
    test_guilds=tml["id"]["guilds"],
    intents=disnake.Intents.all(),
    status=disnake.Activity(name=tml["status"]["message"],type=disnake.ActivityType.watching))

@bot.event
async def on_ready():
    loggercmd.debug(f"'{bot.user.name}#{bot.user.discriminator}' is ready!")

# @bot.event
# async def on_error(event,*args, **kwargs):
#     loggercmd.error(event+args+kwargs)
#     pass


for cog in tml["cogs"]["devcogs"]:
    bot.load_extension(f"devcogs.{cog}",)

for cog in os.listdir("cogs"):
    if os.path.isfile(f"cogs/{cog}") and cog not in tml["cogs"]["disabled"]: 
        bot.load_extension(f"cogs.{cog.split('.')[0]}",)

print("running")
bot.run(os.environ["DISBOTTOKEN1"])
