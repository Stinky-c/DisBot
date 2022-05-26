import disnake
from disnake.ext import commands
import logging
from views import VcView


class MusicPlayerCog(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.loggerl2 = logging.getLogger("disnakecommands.music.cmd")

    @commands.slash_command()
    async def music(self, inter):
        self.loggerl2.info(f"{inter.user.name} ran a command")  # sub command logger

        pass

    @music.sub_command()
    async def load(self, inter: disnake.CmdInter, channel: disnake.VoiceChannel):
        vc: disnake.VoiceClient = await channel.connect()
        await inter.send(
            "Connected!", view=VcView(timeout=None, vc=vc, inter=inter, bot=self.bot)
        )

    async def cog_load(self):
        # async functions here
        pass


def setup(bot):
    logging.getLogger("disnakecommands.music").info(
        f"{__name__} is online"
    )  # init logger
    bot.add_cog(MusicPlayerCog(bot), override=True)
