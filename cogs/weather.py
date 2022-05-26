import disnake
from disnake.ext import commands
import os
import json as js
import io
import logging
import aiohttp


class Greetings(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.loggerl2 = logging.getLogger("disnakecommands.wttr.cmd")
        self.bot = bot
        self.aiohttp = aiohttp.ClientSession()

    @commands.slash_command()
    async def wttr(self, inter: disnake.CmdInter):
        self.loggerl2.info(f"'{inter.user.name}' ran a command")  # sub command logger
        pass

    # ephemeral=True

    # cmd: City
    @wttr.sub_command(description="Returns the weather for the city")
    async def city(
        self,
        inter: disnake.CmdInter,
        city: str,
    ):
        """City - Returns the city

        Args:
            city (str): name of a city
            ephemeral (bool): True
        """
        link = f"https://wttr.in/{city}?T?0?q"
        with self.aiohttp.get(link) as res:
            await inter.send(f"```\n{res.content.decode()}\n```", ephemeral=True)

    # cmd: file
    @wttr.sub_command(
        description="Returns the weather for the city in the json file format. WILL NOT BE HIDDEN"
    )
    async def file(self, inter: disnake.CmdInter, city: str):
        """Json - uploads the format 1 json file

        Args:
            city (str): Name of a city
        """
        link = f"https://wttr.in/{city}?format=j1"
        with self.aiohttp.get(link) as res:
            await inter.send(f"here is the json to {link}")
            await inter.channel.send(
                file=disnake.File(io.BytesIO(res.content), "response.json")
            )

    # cmd: help
    # TODO rewrite ; use dict embed builder
    @wttr.sub_command(description="Returns the weather help message")
    async def help(self, inter: disnake.CmdInter):
        """Help - Returns the help embed

        Args:
        """
        embed = disnake.Embed(
            title="Help", description="The Weather sub command help ", color=0xFF7600
        )
        with open(f"{os.path.dirname(__file__)}/data/help.json") as f:
            tmp = js.load(f)
            for i in tmp:
                embed.add_field(name=i["name"], value=i["value"], inline=i["inline"])
        await inter.send(embed=embed, ephemeral=True)


def setup(bot):
    logging.getLogger("disnakecommands.wttr").info(
        f"{__name__} is online"
    )  # init logger
    bot.add_cog(Greetings(bot), override=True)
