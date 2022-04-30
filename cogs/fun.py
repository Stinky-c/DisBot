import discord
import io
import requests as re
import random as rnd

class FunCog(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    fun = discord.SlashCommandGroup("fun","Various fun commands")


# cmd: would you rather
    @fun.command(description="Would you rather game")
    async def wouldyourather(self,ctx):
        res = re.get("https://api.aakhilv.me/fun/wyr")
        await ctx.respond(res.json()[0])


    # https://github.com/public-apis/public-apis#animals
# cmd: dogsaas
    @fun.command(description="Dogs as a Service")
    async def dogsaas(self,ctx):
        res = re.get("https://dog.ceo/api/breeds/image/random")
        await ctx.respond("here is a dog :)")
        await ctx.send(res.json()["message"])

# cmd: catsaas
    @fun.command(description="Cats as a Service")
    async def catsaas(self,ctx):
        res = re.get("https://cataas.com/cat")
        await ctx.respond("here is a cat :)")
        res.json()
        await ctx.send(file=discord.File(io.BytesIO(res.content),"cat.jpg"))

#cmd: catboy
    @fun.command(description="Returns a catboy")
    async def catboy(self,ctx):
        res = re.get("https://api.catboys.com/img")
        await ctx.respond(res.json()["url"])

# cmd: cat link
    @fun.command(description="Cat as a Service; link")
    async def catlink(self,ctx):
        res = re.get("https://cataas.com/cat?json=true")
        await ctx.respond(f"https://cataas.com{res.json()['url']}")

#cmd: fun fact
    @fun.command(description="fun facts!")
    async def funfact(self,ctx):
        res = re.get("https://api.aakhilv.me/fun/facts")
        await ctx.respond(res.json()[0])

# cmd: RPS
    @fun.command(description="RPS")
    async def rps(self,ctx,choice:discord.Option(str,choices=["rock","paper","scissors"])):
        # :rock: 🪨
        # :roll_of_paper: 🧻
        # :scissors: ✂️
        await ctx.respond(f"You {rnd.choice(['won','lost','tied'])}!")


def setup(bot): 
    
    bot.add_cog(FunCog(bot),override=True) 