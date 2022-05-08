from datetime import datetime
import disnake
import aiohttp
from disnake.ext import commands
from bs4 import BeautifulSoup
import requests as req
import random as rnd
import json
import os
from urllib import parse
import io
import tempfile
import re
import urllib
from pytube import YouTube
import logging
from dotenv import load_dotenv
load_dotenv()
'''
class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None
    @discord.ui.button(label="Vote A",row=0, style=discord.ButtonStyle.red,)
    async def one_button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the first button!")
    @discord.ui.button(label="Vote B",row=0, style=discord.ButtonStyle.red,)
    async def two_button_callback(self, button, interaction):
        og = interaction.message.content
        await interaction.message.edit(og+"1")
        button.label = button.label+"1"
        button.refresh_state(interaction)
'''

class LinkView(disnake.ui.View):
    '''
    Takes list of tuples to add buttons addcordingly
    `[("Label","Link"),("label2","link2")]`
    or a singular tuple following the same scheme
    `("label","link")`
    '''
    def __init__(self, link:tuple=None,links:list=None):
        super().__init__()
        if link:
            self.add_item(disnake.ui.Button(label=link[0],url=link[1],style=disnake.ButtonStyle.link))
        if links:
            for i in links:  
                self.add_item(disnake.ui.Button(label=i[0],url=i[1],style=disnake.ButtonStyle.link))


class DevCog(commands.Cog):

    def __init__(self, bot:commands.InteractionBot):
        self.bot = bot
        self.urlreg = re.compile(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))") 
        self.loggerl2 = logging.getLogger("disnakecommands.dev.cmd")
        self.redditreg = re.compile(r"https://www\.reddit\.com/r/.*")
        self.aioclient = aiohttp.ClientSession()




    @commands.slash_command()
    async def dev(self,inter:disnake.CmdInter):
        self.loggerl2.info(f"'{inter.user.name}' ran a command") # sub command logger
        pass

    @dev.slash_command()
    async def ping(self,inter:disnake.CmdInter):
        if not await self.bot.is_owner(inter.author):
            inter.send("Oh, you're not Bucky")
            return
        await inter.send(f"Pong!\n```{self.bot.latency}```")

    @commands.user_command()
    async def avatar(self,inter:disnake.CmdInter, user:disnake.Member):
        embed_dict = {
        "title": "Embed Title",
        "description": "Embed Description",
        "color": 0xFEE75C,
        "timestamp": datetime.now().isoformat(),
        "author": {
            "name": self.bot.user.name,
            "url": "https://github.com/Stinky-c/",
            "icon_url": "https://raw.githubusercontent.com/Stinky-c/Stinky-c/main/svg/it-just-works-somehow.png",
        },
        "thumbnail": {"url": self.bot.user.display_avatar.url},
        "fields": [
            {"name": "Name", "value": user.name, "inline": "false"},
            {"name": "Inline Title", "value": "Inline Value", "inline": "false"},
            {"name": "Account creation date", "value": disnake.utils.snowflake_time(user.id).strftime("%a %b %d at %I:%M:%S UTC"), "inline": "false"},
        ],
        "image": {"url": user.display_avatar.url},
        "footer": {"icon_url": "https://raw.githubusercontent.com/Stinky-c/Stinky-c/main/svg/it-just-works-somehow.png"},
        }

        await inter.response.send_message(embed=disnake.Embed.from_dict(embed_dict))

    @commands.user_command(name="View Song")
    async def spotifysong(self,inter:disnake.CmdInter,user:disnake.Member):
        if not any(isinstance(x, disnake.Spotify) for x in list(user.activities)):
            await inter.send("That person is not listening to spotify",ephemeral=True)
            return

        spot = next((x for x in list(user.activities) if isinstance(x,disnake.Spotify)), None)
        embed_dict = {
            "type": "image",
            "title": spot.title,
            "description": ", ".join(spot.artists),
            "color": spot.color.value,
            "image": {"url": spot.album_cover_url},
        }
        await inter.send(embed=disnake.Embed.from_dict(embed_dict),view=LinkView(link=("Track Link",spot.track_url)))
        self.loggerl2.info(f"{user.name} is listening to '{spot.title}' by '{spot.artists}' on spotify\nLink{spot.track_url}")
    options = ["playing","streaming","listening","watching","custom","competing"]
    @dev.sub_command()
    async def setactivity(self,inter:disnake.CmdInter,name:str,type:str = commands.Param(choices=options),):
        if not await self.bot.is_owner(inter.author):
            await inter.send("You are not Bucky!") 
            return

        match type:
            case "playing":
                newact = disnake.Activity(name=name,type=disnake.ActivityType.playing)
            case "streaming":
                newact = disnake.Activity(name=name,type=disnake.ActivityType.streaming)
            case "listening":
                newact = disnake.Activity(name=name,type=disnake.ActivityType.listening)
            case "watching":
                newact = disnake.Activity(name=name,type=disnake.ActivityType.watching,)
            case "custom":
                newact = disnake.Activity(name=name,type=disnake.ActivityType.custom)
            case "competing":
                newact = disnake.Activity(name=name,type=disnake.ActivityType.competing)
            case _:
                newact = disnake.Activity(name="Unknown",activity=disnake.ActivityType.custom)
        self.loggerl2.info(f"setting activity to '{newact}'")
        await self.bot.change_presence(activity=newact,status=disnake.Status.idle)
        await inter.send(f"Presence set to `{type} {name}` ")




    '''

    message will look like:

    Would you rather turn into a dog every time you sneeze or a buffalo every time you hiccup?
    ```
    Votes
    A: 72
    B: 9
    ```

    Gets the line a is on `^A: [0-9]*`
    Gets the line b is on `^B: [0-9]*`

    gets the number on the line: ` \d*$`

    TODO: increment the number on a line for every vote
    https://www.geeksforgeeks.org/python-program-to-increment-suffix-number-in-string/

    '''


    '''
    # @dev.sub_command(description="Would you rather game")
    async def wouldyourather(self,ctx):
        res = req.get("https://api.aakhilv.me/fun/wyr")
        # await ctx.response.send_message(res.json()[0])
        message = f"{res.json()}\n```\nA: 0\nB: 0```"
        await ctx.response.send_message(message,view=View())
    '''


    # @dev.sub_command(description="url scr")
    async def urlscan(self,inter:disnake.CmdInter,link:str):
        if re.match(self.urlreg,link):
            # headers = {'API-Key':'$apikey','Content-Type':'application/json'}
            headers = {'Content-Type':'application/json'}
            data = {"url": link, "visibility": "unlisted"}
            response = req.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
            print(response.json())
            await inter.response.send_message(link)
        else:
            await inter.response.send_message("bucky is stupid")


# TODO fix
# @fun.sub_command(description="Axolotl as a Service")
# async def axolotlaas(self,ctx,funfact:disnake.Option(str,choices=["funfact"],required=False)):
#     res = re.get("https://axoltlapi.herokuapp.com/")
#     print(funfact)
#     message = f"here is a axolotl :)\nfun fact {res.json()['facts']}" if funfact else "here is a axolotl :)"
#     await ctx.response.send_message(message)
#     await ctx.send(res.json()["url"])


def setup(bot):
    logging.getLogger("disnakecommands.dev").info(f"{__name__} is online") # init logger
    bot.add_cog(DevCog(bot)) 