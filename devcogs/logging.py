import discord


class LogCog(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    logs = discord.SlashCommandGroup("debug","Various debug commands")

def setup(bot): 
    
    # bot.add_cog(LogCog(bot),override=True) 
    pass