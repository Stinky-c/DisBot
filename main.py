import os
import disnake
from disnake.ext import commands
import anyconfig
import random as rnd
from definitions import *

import logging
from dotenv import load_dotenv
load_dotenv()
tml = anyconfig.load("./config.toml")



#alias
logconf =  tml["logging"]
chance = tml['random']

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


if logconf["verboseenabled"]:
    @bot.event
    async def on_slash_command_error(inter:disnake.CmdInter,error,*args, **kwargs):
        await inter.send("This command errored, Sorry")
        chan = bot.get_channel(logconf["erorrchannel"])
        await chan.send(error)
        loggercmd.error(f"a command errored in '{inter.guild}' '#{inter.channel}'\nargs: '{args}'kwargs: \n{kwargs}")

@bot.event
async def on_message(message:disnake.Message):
    if rnd.randint(chance["min"],chance["max"]) == 3 and tml["random"]["enabled"]:
        await message.add_reaction('🐄')
        loggercmd.info(f"'{message.id}' in '{message.channel}' rolled the dice and won\n'{message.jump_url}'")
# I added it talan
    if bot.user.mentioned_in(message):
        await message.channel.send(rnd.choice(tml["quotes"]["closequotes"]))

for cog in tml["cogs"]["devcogs"]:
    bot.load_extension(f"devcogs.{cog}",)

for cog in os.listdir("cogs"):
    if cog.endswith(".py") and cog not in tml["cogs"]["disabled"]: 
        bot.load_extension(f"cogs.{cog.split('.')[0]}",)

print("running")
bot.run(os.environ["DISBOTTOKEN1"])
