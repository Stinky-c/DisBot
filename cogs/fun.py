import disnake
from disnake.ext import commands
import io
import requests as re
import random as rnd
import os 
import json
import urllib

LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "Rust", "Lisp", "Elixir"]
path = f"{os.path.dirname(__file__)}/data/random/{rnd.choice(os.listdir(os.path.dirname(__file__)+'/data/random/'))}"
with open(path) as f:
    fuckjs:dict = json.load(f)
    howfuck:list=[]
for fucking in fuckjs:
    howfuck.append(fucking["name"])

class FunCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def fun(self,inter):
        # Logging here
        # called everytime a sub command is called
        pass


# cmd: would you rather
    @fun.sub_command(description="Would you rather game")
    async def wouldyourather(self,inter):
        res = re.get("https://api.aakhilv.me/fun/wyr")
        await inter.respond(res.json()[0])

# cmd: fuck

    
    @commands.slash_command()
    async def languages(inter: disnake.CommandInteraction, language:str = commands.Param(choices=LANGUAGES)):
        await inter.response.send_message(language)
    
    
    # @languages.autocomplete("language")
    # async def language_autocomp(inter: disnake.CommandInteraction, string: str):
    #     string = string.lower()
    #     return [lang for lang in LANGUAGES if string in lang.lower()]

    @fun.sub_command(description="fuck")
    async def fuck(self,inter:disnake.CommandInteraction ,to:disnake.User,method:str = commands.Param(choices=howfuck)):
        for i in fuckjs:
            if i["name"] == method:
                link="https://foaas.com"+urllib.parse.quote(i["url"].format(name=to.name,from_=inter.user.name))
                message = f"<@{to.id}>\n{link}"
                await inter.response.send_message(message)

    # https://github.com/public-apis/public-apis#animals
# cmd: dogsaas
    @fun.sub_command(description="Dogs as a Service")
    async def dogsaas(self,inter):
        res = re.get("https://dog.ceo/api/breeds/image/random")
        await inter.respond("here is a dog :)")
        await inter.send(res.json()["message"])

# cmd: catsaas
    @fun.sub_command(description="Cats as a Service")
    async def catsaas(self,inter):
        res = re.get("https://cataas.com/cat")
        await inter.respond("here is a cat :)")
        await inter.send(file=disnake.File(io.BytesIO(res.content),"cat.jpg"))

# cmd: foxaas
    @fun.sub_command(description="Foxes as a Service")
    async def foxaas(self,inter):
        res = re.get("https://randomfox.ca/floof/")
        await inter.respond("here is a fox :)")
        await inter.send(res.json()["image"])

# cmd: duckaas
    @fun.sub_command(description="Ducks as a Service")
    async def duckaas(self,inter):
        res = re.get("https://random-d.uk/api/v2/random")
        await inter.respond("here is a duck :)")
        await inter.send(res.json()["url"])

# cmd: axolotlaas
    @fun.sub_command(description="Axolotl as a Service")
    async def axolotlaas(self,inter,):
        res = re.get("https://axoltlapi.herokuapp.com/")
        await inter.respond("here is a axolotl :)")
        await inter.send(res.json()["url"])

# cmd: catboy
    @fun.sub_command(description="Returns a catboy")
    async def catboy(self,inter):
        res = re.get("https://api.catboys.com/img")
        await inter.respond(res.json()["url"])

# cmd: animefacts
    @fun.sub_command()
    async def animefacts(self,inter):
        res = re.get("https://animechan.vercel.app/api/random")
        await inter.respond(f"{res.json()['character']}: {res.json()['quote']}\n- {res.json()['anime']}")

# cmd: cat link
    @fun.sub_command(description="Cat as a Service; link")
    async def catlink(self,inter):
        res = re.get("https://cataas.com/cat?json=true")
        await inter.respond(f"https://cataas.com{res.json()['url']}")

#cmd: fun fact
    @fun.sub_command(description="fun facts!")
    async def funfact(self,inter):
        res = re.get("https://api.aakhilv.me/fun/facts")
        await inter.respond(res.json()[0])

# cmd: color

# cmd: RPS
'''    @fun.sub_command(description="RPS")
    async def rps(self,inter,choice:disnake.Option(str,choices=["rock","paper","scissors"])):
        # :rock: 🪨
        # :roll_of_paper: 🧻
        # :scissors: ✂️
        await inter.respond(f"You {rnd.choice(['won','lost','tied'])}!")'''


def setup(bot): 
    
    bot.add_cog(FunCog(bot),override=True) 