import discord


class RenameMeCog(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    renameMe = discord.SlashCommandGroup("debug","Various debug commands")


def setup(bot): 
    
    bot.add_cog(RenameMeCog(bot),override=True) 