import os
import disnake
from disnake.ext import commands
import anyconfig
import random as rnd

import logging
from dotenv import load_dotenv
load_dotenv()
tml = anyconfig.load("./config.toml")


# https://docs.python.org/3/library/logging.html#module-logging

logconf =  tml["logging"]
logger = logging.getLogger('disnake')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=logconf["bot"]["path"], encoding=logconf["encoding"], mode=logconf["method"])
handler.setFormatter(logging.Formatter(logconf["bot"]["format"]))
logger.addHandler(handler)

loggercmd = logging.getLogger("disnakecommands")
loggercmd.setLevel(logging.INFO)
handlercmd = logging.FileHandler(filename=logconf["commands"]["path"], encoding=logconf["encoding"], mode=logconf["method"])
handlercmd.setFormatter(logging.Formatter(logconf["commands"]["format"]))
loggercmd.addHandler(handlercmd)
loggercmd = logging.getLogger("disnakecommands.main")

bot = commands.InteractionBot(
    sync_commands_debug=True,
    owner_ids=tml["id"]["ownerids"],
    test_guilds=tml["id"]["guilds"],
    intents=disnake.Intents.all(),
    activity=disnake.Activity(
        name=tml["status"]["message"],
        type=getattr(disnake.ActivityType,tml["status"]["type"])
        ),
    status=getattr(disnake.Status,tml["status"]["status"])
    )

@bot.event
async def on_ready():
    loggercmd.debug(f"'{bot.user.name}#{bot.user.discriminator}' is ready!")

# @bot.event
# async def on_error(event,*args, **kwargs):
#     loggercmd.error(event+args+kwargs)
#     pass

@bot.event
async def on_message(message:disnake.Message):
    chance = tml['random']
    if rnd.randint(chance["min"],chance["max"]) == 3:
        await message.add_reaction('🐄')
        loggercmd.info(f"'{message.id}' in '{message.channel}' rolled the dice and won\n'{message.jump_url}'")

for cog in tml["cogs"]["devcogs"]:
    bot.load_extension(f"devcogs.{cog}",)

for cog in os.listdir("cogs"):
    if os.path.isfile(f"cogs/{cog}") and cog not in tml["cogs"]["disabled"]: 
        bot.load_extension(f"cogs.{cog.split('.')[0]}",)

print("running")
bot.run(os.environ["DISBOTTOKEN1"])
