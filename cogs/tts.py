import disnake
from disnake.ext import commands
import logging
from views.tts import TTSView


class TTS(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.loggerl2 = logging.getLogger("disnakecommands.TTS.cmd")

    @commands.slash_command()
    async def tts(self, inter):
        self.loggerl2.info(f"{inter.user.name} ran a command")  # sub command logger

    @tts.sub_command(description="Starts the TTS connection")
    async def start(self, inter: disnake.CmdInter, channel: disnake.VoiceChannel):
        try:
            vc: disnake.VoiceClient = await channel.connect()
        except disnake.ClientException:
            await inter.send("I am already connected you fool!")
            return
        await inter.send(
            f"Connected to <#{channel.id}>",
            view=TTSView(vc=vc, inter=inter, bot=self.bot, logger=self.loggerl2),
        )


def setup(bot):
    logging.getLogger("disnakecommands.TTS").info(
        f"{__name__} is online"
    )  # init logger
    bot.add_cog(TTS(bot), override=True)
