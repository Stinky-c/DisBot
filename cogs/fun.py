from bs4 import BeautifulSoup
from urllib import parse
import time
import disnake
from disnake.ext import commands
from pytube import YouTube
import tempfile
import io
import re
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

class FunCog(commands.Cog):

    def __init__(self, bot):
        self.loggerl2 = logging.getLogger("disnakecommands.fun.cmd")
        self.urlreg = re.compile(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))") 
        self.redditreg = re.compile(r"https://www\.reddit\.com/r/.*")
        self.bot = bot

    @commands.slash_command()
    async def fun(self,inter:disnake.CmdInter):
        self.loggerl2.info(f"'{inter.user.name}' ran a command") # sub command logger

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
            vids = yt.streams.order_by("resolution").desc().filter(type="video",progressive=True,mime_type="video/mp4",)
            if len(vids) == 0:
                self.loggerl2.info(f"{yt.title} cannot be downloaded due to invaild filters")
                await inter.send(f"{yt.title} cannot be downloaded due to invaild filters")
                return

            for vid in vids:
                if vid.filesize_approx <= 8388608:
                    break

            if vid.filesize_approx >= 8388608:
                self.loggerl2.info(f"{yt.title} cannot be downloaded due to invaild filters")
                await inter.send(f"{yt.title} cannot be downloaded due to invaild filters")
                return

            with tempfile.TemporaryDirectory() as td:
                self.loggerl2.info(f"'{inter.user.name}' downloaded '{yt.title}'; size: {round(vid.filesize_approx/1024,5)}kb\ndata: '{vid}'")
                await inter.send(file=disnake.File(vid.download(td)))
                return
        except Exception as e:
            self.loggerl2.error(e)
            self.loggerl2.error(f"downloading '{yt.title}' has errored")
            await inter.send("Something went ***really*** wrong\nPlease contact Bucky")

# cmd : redditdownload
# TODO move this command to its own cog and fix it
    @fun.sub_command()
    async def redditdownload(self,inter:disnake.CmdInter,link:str):
        if not re.match(self.redditreg,link):
            await inter.send("Please provide a valid link\n Example:`https://www.reddit.com/r/blurrypicturesofcats/comments/uigcmv/blurry_picture_of_a_cat/` or `https://www.reddit.com/r/blurrypicturesofcats/comments/uigcmv/`")
            return

        link2 = "https://redditsave.com/info?url="+parse.quote(link)
        print(link2)
        soup = BeautifulSoup(req.get(link2).content, 'html.parser')
        download = soup.find("div", {"class": "download-info"}).find("a").get("href") if not soup.find("div", {"class": "alert alert-danger"}) else None
        if download is None:
            await inter.send("Something went ***really*** wrong\nPlease contact Bucky")
            return
        await inter.response.defer()
        res = req.get(download)
        if int(res.headers.get("Content-Length")) >= 8388608:
            await inter.send(f"The file is too large\nHere is the link {download}")
            return
        currnettime=str(time.time()).split(".")[0]
        
        await inter.send(file=disnake.File(io.BytesIO(res.content),currnettime+".jpg" if res.headers.get("Content-Type") == "image/jpeg" else currnettime+".mp4"))
        self.loggerl2.info(f"'{inter.user.name}' downloaded a reddit video size: {round(int(res.headers.get('Content-Length'))/1024,5)}kb\nurl: '{download}'")

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