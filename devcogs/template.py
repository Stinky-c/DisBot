import disnake
from disnake.ext import commands


class RenameMeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def RenameMe(self,inter):
        # Logging here
        # called everytime a sub command is called
        pass


def setup(bot): 
    
    bot.add_cog(RenameMeCog(bot),override=True) 