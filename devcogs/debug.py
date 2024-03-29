import asyncio
from datetime import datetime
import disnake
from disnake.ext import commands
import requests as req
import os
from dotenv import load_dotenv

load_dotenv()
import logging


class DebugCog(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.loggerl2 = logging.getLogger("disnakecommands.debug.cmd")
        self.bot = bot

    @commands.slash_command()
    async def debug(self, inter: disnake.CmdInter):
        if not await self.bot.is_owner(inter.author):
            return
        self.loggerl2.info(f"'{inter.user.name}' ran a command")  # sub command logger
        pass

    @debug.sub_command(description="Echo Echo Echo - Bucky only")
    async def echo(self, inter: disnake.CmdInter, message: str):
        if self.bot.is_owner(inter.author):
            await inter.response.send_message(
                "You cannot use this command", ephemeral=True
            )
            return
        pass
        await inter.channel.send(message)
        await inter.send("Sent!", ephemeral=True)

    @debug.sub_command(description="Sends the server ip - Bucky only")
    async def sendipforserver(self, inter: disnake.CmdInter):
        if self.bot.is_owner(inter.author):
            await inter.response.send_message(
                req.get("https://icanhazip.com/").content.decode(), ephemeral=True
            )
            self.loggerl2.info(
                f"{inter.author.name}#{inter.author.discriminator} @ {datetime.now()} in {inter.guild} #{inter.channel}"
            )
        else:
            self.loggerl2.info(
                f"failed: {inter.author.name}#{inter.author.discriminator} @ {datetime.now()} in {inter.guild} #{inter.channel}"
            )
            await inter.response.send_message(
                "no stupid\nonly bucky can do that and ive already told him what youre trying to do"
            )
        pass


def setup(bot):
    logging.getLogger("disnakecommands.debug").info(
        f"{__name__} is online"
    )  # init logger
    bot.add_cog(DebugCog(bot), override=True)
