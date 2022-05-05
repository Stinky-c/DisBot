import disnake
from disnake.ext import commands
from pytube import YouTube
import tempfile
import io
import requests as re
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

class FunCog(commands.Cog):

    def __init__(self, bot):
        self.loggerl2 = logging.getLogger("disnakecommands.fun.cmd")

        self.bot = bot

    @commands.slash_command()
    async def fun(self,inter:disnake.CmdInter):
        self.loggerl2.info(f"{inter.user.name} ran a command") # sub command logger

        pass

# cmd: youtubedownload
# TODO write sort algorithm for file size or give options
# IDEA add filesize to pytube stream object
    @fun.sub_command(description="Downloads a YouTube video from a link returning the best video under 8mb")
    async def youtubedownload(self,inter:disnake.CmdInter,link:str):
        try:
            if not re.match(self.urlreg,link):
                await inter.send("Please provide a valid link\n Example:`https://www.youtube.com/watch?v=dQw4w9WgXcQ` or `https://youtu.be/dQw4w9WgXcQ`")
                return
            yt = YouTube(link)
            await inter.response.defer()
            for vid in yt.streams.order_by("resolution").desc().filter(file_extension="mp4",only_video=True,progressive=False,video_codec="avc1.4d4015"):
                if vid.filesize <= 8388608:
                    break
            if vid.filesize >= 8388608:
                await inter.send("This video cannot be downloaded due to its size. Please try a smaller one")
                self.loggerl2.error(f"'{yt.title}' is too large ; data: {vid}")
                return
            with tempfile.TemporaryDirectory() as td:
                self.loggerl2.info(f"'{inter.user.name}' downloaded '{yt.title}'; size: {round(vid.filesize/1024,5)}kb, data: '{vid}'")
                await inter.send(file=disnake.File(vid.download(td)))
                return
        except Exception as e:
            self.loggerl2.error(e)
            await inter.send("Something went ***really*** wrong\nPlease contact Bucky")

# cmd: would you rather
    @fun.sub_command(description="Would you rather game")
    async def wouldyourather(self,inter:disnake.CmdInter):
        res = re.get("https://api.aakhilv.me/fun/wyr")
        await inter.send(res.json()[0])

# cmd: fuck
# TODO rewrite this
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
    async def dogsaas(self,inter:disnake.CmdInter):
        res = re.get("https://dog.ceo/api/breeds/image/random")
        await inter.send("here is a dog :)")
        await inter.channel.send(res.json()["message"])

# cmd: catsaas
    @fun.sub_command(description="Cats as a Service")
    async def catsaas(self,inter:disnake.CmdInter):
        res = re.get("https://cataas.com/cat")
        await inter.send("here is a cat :)")
        await inter.channel.send(file=disnake.File(io.BytesIO(res.content),"cat.jpg"))

# cmd: foxaas
    @fun.sub_command(description="Foxes as a Service")
    async def foxaas(self,inter:disnake.CmdInter):
        res = re.get("https://randomfox.ca/floof/")
        await inter.send("here is a fox :)")
        await inter.channel.send(res.json()["image"])

# cmd: duckaas
    @fun.sub_command(description="Ducks as a Service")
    async def duckaas(self,inter:disnake.CmdInter):
        res = re.get("https://random-d.uk/api/v2/random")
        await inter.send("here is a duck :)")
        await inter.channel.send(res.json()["url"])

# cmd: axolotlaas
    @fun.sub_command(description="Axolotl as a Service")
    async def axolotlaas(self,inter:disnake.CmdInter):
        res = re.get("https://axoltlapi.herokuapp.com/")
        await inter.send("here is a axolotl :)")
        await inter.channel.send(res.json()["url"])

# cmd: catboy
    @fun.sub_command(description="Returns a catboy")
    async def catboy(self,inter:disnake.CmdInter):
        res = re.get("https://api.catboys.com/img")
        await inter.send(res.json()["url"])

# cmd: animefacts
    @fun.sub_command()
    async def animefacts(self,inter:disnake.CmdInter):
        res = re.get("https://animechan.vercel.app/api/random")
        await inter.send(f"{res.json()['character']}: {res.json()['quote']}\n- {res.json()['anime']}")

# cmd: cat link
    @fun.sub_command(description="Cat as a Service; link")
    async def catlink(self,inter:disnake.CmdInter):
        res = re.get("https://cataas.com/cat?json=true")
        await inter.respond(f"https://cataas.com{res.json()['url']}")

#cmd: fun fact
    @fun.sub_command(description="fun facts!")
    async def funfact(self,inter:disnake.CmdInter):
        res = re.get("https://api.aakhilv.me/fun/facts")
        await inter.send(res.json()[0])

# cmd: color

# cmd: RPS
    @fun.sub_command(description="RPS")
    async def rps(self,inter:disnake.CmdInter,choice:str=commands.Param(choices=["rock","paper","scissors"])):
        # :rock: 🪨
        # :roll_of_paper: 🧻
        # :scissors: ✂️
        await inter.response.send_message(f"You {rnd.choice(['won','lost','tied'])}!")


def setup(bot): 
    logging.getLogger("disnakecommands.fun").info(f"{__name__} is online") # init logger
    bot.add_cog(FunCog(bot),override=True) 