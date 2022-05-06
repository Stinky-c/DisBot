import disnake
from disnake.ext import commands
import logging

class RenameMeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def RenameMe(self,inter):
        self.loggerl2.info(f"{inter.user.name} ran a command") # sub command logger

        pass


def setup(bot): 
    logging.getLogger("disnakecommands.RENAMEME").info(f"{__name__} is online") # init logger
    bot.add_cog(RenameMeCog(bot),override=True) 