from bs4 import BeautifulSoup
from urllib import parse
import random 
import disnake
from disnake.ext import commands
from pytube import YouTube
import tempfile
import io
import re
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
        self.quotes = [
            "Cave Johnson here, Science isn't about why, it's about why not.",
            "I’ve come to a point in my life where I need a stronger word than fuck",
            "With great power comes great need to take a nap. Wake me up later.",
            "Fool me once, I’m gonna kill you",
            "If I see a bug, I simply leave the room elegantly and require someone else do something about it. If no one fulfills my wish, I simply never go back in there.",
            "Well, well, well, if it isn't the consequences of my actions.",
            "Well, well, well... if it isn’t my old friend: the dawning realization that I fucked up bad."
            "I was born for politics. I have great hair and I love lying.",
            "Sometimes I wonder if I'm hearing voices. Then I remember that's the last bit of sanity I have trying to get me to fall asleep at a reasonable time.",
            "I am very small and I have no money, so you can imagine the kind of stress that I'm under.",
            "I've never encountered a problem that can't be solved by an spontaneous musical number.",
            "I scare people a lot because I walk very softly and they don't hear me enter rooms. So when they turn around, I'm just kind of there and their fear fuels me.",
            "Well, needless to say. Uh-oh Spaghetti-os.",
            "I will send my army to attack! *releases a dumpster of raccoons*",
            "And remember, if I get harsh with you it is only because you're doing it all wrong.",
            "I'm allergic to death.",
            "I'm a firm believer in \"if you're going to fail, you might as well fail spectacularly.\"",
            "As someone who has a long history of not understanding anything, I feel confident in my ability to continue not knowing what is going on.",
            "Fruits that do not live up to their names; passionfruit, grapefruit, honeydew and dragonfruit. Fruits that do live up to their names? Orange.",
            "Can I offer you a nice stick in this trying time?",
            "Firstly, how dare you use mathematics to make me look stupid! I'm actually very good at mathematics. Thirdly, I think you might be right.",
            "I'm not a morning person. I'm barely even a person.",
            "I warned you. I'm perfect.",
            "We got a free day now. What do you wanna do? Eat? Sleep? Nap? Snack?",
            "Underestimate me. That'll be fun.",
            "I don't follow the rules. I follow dogs on social media.",
            "I like to play this game called nap roulette. I take a nap and don't set an alarm. Will it be 20 min or 4 hours? Nobody knows. It's risky and I like it.",
            "It began as a mistake",
            "Atoms can never touch each other, and we are made of atoms, therefore no I did not push the baby.",
            "If you buy a bigger bed, you're left with more bed room, but less bedroom.",
            "I may be able to stand, but I cant stand this",
            "*Monkey noises*",
            "If a fly didn't have wings, would it be called a walk?",
            "It's not ugly, just aesthetically challenged.",
            "I have a philosophy in life; if the seat is open, the job is open. That’s how I came to briefly drive a Formula 1 car.",
            "Do you ever think? Because I do not.",
            "Don't worry, I have your phone! Text me when you're gonna come get it!",
            "Physically, yes, I could fight a bird. But emotionally? Imagine the toll.",
            "People are always asking me if I'm a morning person or a night person. I'm just like, 'Buddy! I'm barely even a PERSON!'",
            "Dear friends, your Christmas gift this year… is me. That’s right, another year of friendship. Your membership has been renewed.",
            "When someone points at your black clothes and asks whose funeral it is, having a look around the room and saying 'Haven’t decided yet' is typically a good response.",
            "Not trying to brag or anything, but I can wake up without an alarm clock now simply due to my crippling and overwhelming anxiety, so...",
            "I’m sick and tired of being called 'mortal' like, you don’t know that. Neither do I. I have never died even ONCE. Nothing has been proven yet. Stop making assumptions. It’s rude.",
            "BEHOLD, the field in which I grow my fucks! Lay thine eyes upon it, and thou shalt see that it is barren!",
            "You seem familiar, have I threatened you before?",
            "Okay okay stop asking me if I'm straight, gay, bi, whatever. I identify as a FUCKING THREAT.",
            "My life isn’t as glamorous as my wanted poster makes it look like."
            ]

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