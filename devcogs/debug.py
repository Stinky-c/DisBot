from datetime import datetime
import discord
import requests as req
import os
from dotenv import load_dotenv
load_dotenv()


class DebugCog(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    debug = discord.SlashCommandGroup("debug","Various debug commands")
    @debug.command(description="test")
    async def test(self,ctx):
        await ctx.respond(ctx)
        async for guild in self.bot.fetch_guilds(limit=150):
            print(guild.name)
            ctx

    @debug.command(description="Stops the bot")
    async def stop(self,ctx):
        if ctx.user.id == 593118233993805834:
            await ctx.respond("Stopping")
            await self.bot.close()
        await ctx.respond("no lol")

    @debug.command()
    async def parrot(self,ctx,message):
        await ctx.respond(message)
        print(message)

    @debug.command(description="for bucky only")
    async def sendipforserver(self,ctx):
        if ctx.author.id == int(os.environ["BUCKYID"]):
            await ctx.respond(req.get("https://icanhazip.com/").content.decode(),ephemeral=True)
            print(f"{ctx.author.name}#{ctx.author.discriminator} @ {datetime.now()} in {ctx.guild} #{ctx.channel}")
        else:
            print(f"failed: {ctx.author.name}#{ctx.author.discriminator} @ {datetime.now()} in {ctx.guild} #{ctx.channel}")
            await ctx.respond("no stupid\nonly bucky can do that and ive already told him what youre trying to do")
        pass


def setup(bot): 
    
    bot.add_cog(DebugCog(bot),override=True) 