from bs4 import BeautifulSoup
from urllib import parse
import random 
import disnake
from disnake.ext import commands
from pytube import YouTube
import tempfile
import io
import anyconfig
import aiohttp
import requests as req
import random as rnd
import os 
import json
import urllib
import logging

path = f"{os.path.dirname(__file__)}/data/random/{rnd.choice(os.listdir(os.path.dirname(__file__)+'/data/random/'))}"
with open(path) as f:
    fuckjs:dict = json.load(f)
    howfuck:list=[]
for fucking in fuckjs:
    howfuck.append(fucking["name"])

class LinkView(disnake.ui.View):
    def __init__(self, link:str):
        super().__init__()
        self.link = link
        self.add_item(disnake.ui.Button(label="Link",url=link,style=disnake.ButtonStyle.green))


class FunCog(commands.Cog):

    def __init__(self, bot:commands.InteractionBot):
        self.loggerl2 = logging.getLogger("disnakecommands.fun.cmd")
        self.bot = bot
        self.aioclient = aiohttp.ClientSession()
        self.configpath = os.path.dirname(__file__)+"/data/config.toml"
        self.quotes = anyconfig.load(self.configpath)["quotes"]["quotes"]

    @commands.slash_command()
    async def fun(self,inter:disnake.CmdInter):
        self.loggerl2.info(f"'{inter.user.name}' ran a command") # sub command logger

        pass


# cmd: would you rather
    @fun.sub_command(description="Would you rather game")
    async def wouldyourather(self,inter:disnake.CmdInter):
        """Would you rather

        Args:
            None
        """
        async with self.aioclient.get("https://api.aakhilv.me/fun/wyr") as res:
            await inter.send((await res.json())[0])

# cmd: fuck
# TODO rewrite this
    @fun.sub_command(description="fuck")
    async def fuck(self,inter:disnake.CmdInter ,to:disnake.User,method:str = commands.Param(choices=howfuck)):
        """FOAAS - Fuck off as a service

        Args:
            to (disnake.User): Who?
            method (str): How? 
        """
        for i in fuckjs:
            if i["name"] == method:
                link="https://foaas.com"+urllib.parse.quote(i["url"].format(name=to.name,from_=inter.user.name))
                message = f"<@{to.id}>\n{link}"
                await inter.response.send_message(message)

    # https://github.com/public-apis/public-apis#animals
# cmd: dogsaas
    @fun.sub_command(description="Dogs as a Service")
    async def dogsaas(self,inter:disnake.CmdInter):
        """DOGAAS - Dogs as a service
        Powered by: `https://dog.ceo/dog-api/`

        Args:
            None
        """
        async with self.aioclient.get("https://dog.ceo/api/breeds/image/random") as res:
            await inter.send("here is a dog :)")
            await inter.channel.send((await res.json())["message"])

# cmd: catsaas
    @fun.sub_command(description="Cats as a Service")
    async def catsaas(self,inter:disnake.CmdInter):
        """CATAAS - Cats as a service
        Powered by: `https://cataas.com/`

        Args:
            None
        """
        async with self.aioclient.get("https://cataas.com/cat") as res:
            await inter.send("here is a cat :)")
            await inter.channel.send(file=disnake.File(io.BytesIO(await res.read()),"cat.jpg"))

# cmd: foxaas
    @fun.sub_command(description="Foxes as a Service")
    async def foxaas(self,inter:disnake.CmdInter):
        """FOXAAS - Foxes as a service 
        Powered by:  `https://randomfox.ca`

        Args:
            None
        """
        async with self.aioclient.get("https://randomfox.ca/floof/") as res:
            await inter.send("here is a fox :)")
            await inter.channel.send((await res.json())["image"])

# cmd: duckaas
    @fun.sub_command(description="Ducks as a Service")
    async def duckaas(self,inter:disnake.CmdInter):
        """DUCKAAS - Ducks as a service
        Powered by: `https://random-d.uk`

        Args:
            None
        """
        async with self.aioclient.get("https://random-d.uk/api/v2/random") as res:
            await inter.send("here is a duck :)")
            await inter.channel.send((await res.json())["url"])

# cmd: axolotlaas
    @fun.sub_command(description="Axolotl as a Service")
    async def axolotlaas(self,inter:disnake.CmdInter):
        """AXOLOTLASS - Axolotls as a service
        api is being reworked 5/5
        https://github.com/AxolotlAPI/what-happened

        Args:
            None
        """
        await inter.send("This is currently being reworked D:\nhttps://github.com/AxolotlAPI/what-happened"); return
        async with self.aioclient.get("https://axoltlapi.herokuapp.com/") as res:
            await inter.send("here is a axolotl :)")
            await inter.channel.send((await res.json())["url"])

# cmd: catboy
    @fun.sub_command(description="Returns a catboy")
    async def catboy(self,inter:disnake.CmdInter):
        """Catboy - Returns a catboy image
        Powered by: `https://api.catboys.com/`
        
        Args:
            None
        """
        async with self.aioclient.get("https://api.catboys.com/img") as res:
            await inter.send((await res.json())["url"])

# cmd: animequotes
    @fun.sub_command(description="Anime quotes")
    async def animequotes(self,inter:disnake.CmdInter):
        """Anime Quotes - Returns an anime quote
        Powered by: `https://animechan.vercel.app`

        Args:
            None
        """
        async with self.aioclient.get("https://animechan.vercel.app/api/random") as res:
            await inter.send(f"{(await res.json())['character']}: {(await res.json())['quote']}\n- {(await res.json())['anime']}")

# cmd: cat link
    @fun.sub_command(description="Cat as a Service; link")
    async def catlink(self,inter:disnake.CmdInter):
        """CATAAS: link - Cats as a service: link
        Powered by: `https://cataas.com`

        Args:
            None
        """
        async with self.aioclient.get("https://cataas.com/cat?json=true") as res:
            await inter.send(f"https://cataas.com{(await res.json())['url']}")

#cmd: fun fact
    @fun.sub_command(description="fun facts!")
    async def funfact(self,inter:disnake.CmdInter):
        """Fun Facts! - returns a fun fact

        Args:
            None
        """
        async with self.aioclient.get("https://api.aakhilv.me/fun/facts") as res:
            await inter.send((await res.json())[0])

# cmd: randomapi
    @fun.sub_command(description="Returns a singular random public api powered by https://api.publicapis.org")
    async def randomapi(self,inter:disnake.CmdInter):
        """Random API - Returns a random public API

        Args:
            None
        """
        async with self.aioclient.get("https://api.publicapis.org/random") as res:
            js = (await res.json()) ["entries"][0]
            await inter.send(f"```Name: {js['API']}\nDescription: {js['Description']}\nAuth: {js['Auth']}\nCORS: {js['Cors']}\nLink: {js['Link']}\n```",view=LinkView(js["Link"]))


# cmd: RPS
    @fun.sub_command(description="RPS")
    async def rps(self,inter:disnake.CmdInter,choice:str=commands.Param(choices=["rock","paper","scissors"])):
        """RPS - Plays rock paper scissors

        Args:
            choice (str): Rock, Paper, or Scissors
        """
        # :rock: 🪨
        # :roll_of_paper: 🧻
        # :scissors: ✂️
        await inter.response.send_message(f"You {rnd.choice(['won','lost','tied'])}!")
    @fun.sub_command()
    async def quote(self,inter:disnake.CmdInter,amount:int=commands.Param(0,lt=15,gt=0)):
        await inter.send("\n".join(random.choices(self.quotes,k=amount)))


def setup(bot): 
    logging.getLogger("disnakecommands.fun").info(f"{__name__} is online") # init logger
    bot.add_cog(FunCog(bot),override=True) 