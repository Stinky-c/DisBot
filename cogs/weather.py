import discord
import os
import requests as re 
import json as js
import io

class Greetings(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    wttr = discord.SlashCommandGroup("weather","Various weather links")
    # ephemeral=True


# cmd: City
    @wttr.command(description="Returns the weather for the city")
    async def city(self,ctx,city:str,):
        link = f"https://wttr.in/{city}?T?0?q"  
        res = re.get(link)
        await ctx.respond(f"```\n{res.content.decode()}\n```",ephemeral=True)


# cmd: file
    @wttr.command(description="Returns the weather for the city in the json file format. WILL NOT BE HIDDEN")
    async def file(self,ctx,city:str):
        link = f"https://wttr.in/{city}?format=j1"
        res = re.get(link)
        await ctx.respond(f"here is the json to {link}")
        await ctx.send(file=discord.File(io.BytesIO(res.content),"response.json"))

# cmd: help
    @wttr.command(description="Returns the weather help message")
    async def help(self,ctx):
        embed=discord.Embed(title="Help", description="The Weather sub command help ", color=0xff7600)
        with open(f"{os.path.dirname(__file__)}/data/help.json") as f:
            tmp = js.load(f)
            for i in tmp:
                embed.add_field(name=i["name"], value=i["value"], inline=i["inline"])
        await ctx.respond(embed=embed,ephemeral=True)

def setup(bot):
    bot.add_cog(Greetings(bot),override=True)