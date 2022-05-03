from datetime import datetime
import disnake
from disnake.ext import commands
import requests as req
import os
from dotenv import load_dotenv
load_dotenv()


class DebugCog(commands.Cog):

    def __init__(self, bot:commands.InteractionBot):
        self.bot = bot


    @commands.slash_command()
    async def debug(self,inter):
        # Here you can paste some code, it will run for every invoked sub-command.
        pass
    @debug.sub_command(description="test")
    async def test(self,ctx):
        await ctx.response.send_message(ctx)
        async for guild in self.bot.fetch_guilds(limit=150):
            print(guild.name)
            ctx

    @debug.sub_command(description="Stops the bot")
    async def stop(self,ctx):
        if ctx.user.id == 593118233993805834:
            await ctx.response.send_message("Stopping")
            await self.bot.close()
        await ctx.response.send_message("no lol")

    @debug.sub_command()
    async def parrot(self,ctx,message):
        await ctx.response.send_message(message)
        print(message)

    @debug.sub_command(description="Echo Echo Echo - Bucky only")
    async def echo(self,ctx,message:str):
        if ctx.author.id != int(os.environ["BUCKYID"]):
            await ctx.response.send_message("You cannot use this command",ephemeral=True)
            return
        pass
        await ctx.channel.send(message)
        await ctx.message.delete()

    @debug.sub_command(description="Sends the server ip - Bucky only")
    async def sendipforserver(self,ctx):
        if ctx.author.id == int(os.environ["BUCKYID"]):
            await ctx.response.send_message(req.get("https://icanhazip.com/").content.decode(),ephemeral=True)
            print(f"{ctx.author.name}#{ctx.author.discriminator} @ {datetime.now()} in {ctx.guild} #{ctx.channel}")
        else:
            print(f"failed: {ctx.author.name}#{ctx.author.discriminator} @ {datetime.now()} in {ctx.guild} #{ctx.channel}")
            await ctx.response.send_message("no stupid\nonly bucky can do that and ive already told him what youre trying to do")
        pass


def setup(bot): 
    
    bot.add_cog(DebugCog(bot),override=True) 