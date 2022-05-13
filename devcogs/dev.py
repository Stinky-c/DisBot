import asyncio
from datetime import datetime
from typing import Optional
import disnake
import aiohttp
from disnake.ext import commands
import requests as req
import random as rnd
import json
import re
import logging
from definitions import *

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
# Welcome to callback hell
class MyModal(disnake.ui.Modal):
    def __init__(self,custom_id):
        components = [
            disnake.ui.TextInput(
                label="Song Link",
                custom_id="link",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
        ]
        super().__init__(
            title="Create Tag",
            custom_id=custom_id,
            components=components,
        )
    async def callback(self, inter: disnake.ModalInteraction):
        await inter.send(f"'{inter.text_values.get('link',None)}' has been added!",ephemeral=True)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
        await inter.send(f"An error occurred!\n```{error}```")
    async def on_timeout(self,):
        pass

class VcView(disnake.ui.View):
    # add some verbose to this
    def __init__(self, *, timeout:Optional[float]=180,vc:disnake.VoiceClient,inter:disnake.CmdInter,bot:commands.Bot):
        super().__init__(timeout=timeout)
        self.vc = vc
        self.inter = inter
        self.bot = bot
        self.info = {
            "playing": False,
            "songs":[
                # list of songs
            ],
            "channel": False
        }

    def poll(self,inter:disnake.CmdInter,*args, **kwargs):
        # updates the message list
        # use a dict and make a function to return it as a usable string
        pass
    @disnake.ui.button(label="Toggle Pause",style=disnake.ButtonStyle.green)
    async def pauseCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        status = self.vc.is_paused()
        match status:
            case True:
                self.vc.resume()
                self.info["playing"] = True
            case False:
                self.vc.pause()
                self.info["playing"] = False

        pass

    @disnake.ui.button(label="Append Song",style=disnake.ButtonStyle.green)
    async def songCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        modid = str(rnd.random())
        await inter.response.send_modal(modal=MyModal(modid))
        mod_inter:disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check= lambda i: i.custom_id == modid and i.author.id == inter.author.id,
            timeout=300
        )
        # poll the songs and append to the list
        # find a way to allow people to reorder the list
        print(mod_inter.text_values.items())
        pass

    @disnake.ui.button(label="Leave",style=disnake.ButtonStyle.red)
    async def leaveCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        await self.vc.disconnect()
        button.disabled = True
        await inter.response.send_message("left!",ephemeral=True)
        await self.inter.delete_original_message(delay=5.0)
        self.stop()

class DevCog(commands.Cog):

    def __init__(self, bot:commands.InteractionBot):
        self.bot = bot
        self.urlreg = re.compile(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))") 
        self.loggerl2 = logging.getLogger("disnakecommands.dev.cmd")
        self.redditreg = re.compile(r"https://www\.reddit\.com/r/.*")
        self.aioclient = aiohttp.ClientSession()
        self.closequotes = ROOT_CONFIG["quotes"]["closequotes"]
        self.talanquotes = ROOT_CONFIG["quotes"]["talanquotes"]



    @commands.slash_command()
    async def dev(self,inter:disnake.CmdInter):
        self.loggerl2.info(f"'{inter.user.name}' ran a command") # sub command logger
        pass

    @dev.sub_command()
    async def stop(self,inter:disnake.CmdInter):
        if not await self.bot.is_owner(inter.author):
            await inter.send("You cant run this command.")
            return
        try:
            await inter.send(rnd.choice(self.closequotes))
            await self.bot.close()
        except Exception:
            pass
    @dev.sub_command()
    async def tell(self,inter:disnake.CmdInter,user:disnake.User):
        if not await self.bot.is_owner(inter.author):
            await inter.send("You are not bucky.",ephemeral=True)
            return
        quote = rnd.choice(self.talanquotes)
        self.loggerl2.info(f"I told '{user.name}' '{quote}'... don't worry")
        await user.send(quote+"\n-Bucky")
        await inter.send("Sent",ephemeral=True)

    @dev.sub_command()
    async def ping(self,inter:disnake.CmdInter):
        if not await self.bot.is_owner(inter.author):
            await inter.send("Oh, you're not Bucky")
            return
        await inter.send(f"Pong!\n```{round(self.bot.latency,5)}```")


    options = ["playing","listening","watching","custom","competing"]
    @dev.sub_command()
    async def setactivity(self,inter:disnake.CmdInter,name:str,type:str = commands.Param(choices=options),):
        if not await self.bot.is_owner(inter.author):
            await inter.send("You are not Bucky!") 
            return

        newact = disnake.Activity(name=name,type=getattr(disnake.ActivityType,type))
        self.loggerl2.info(f"setting activity to '{newact}'")
        await self.bot.change_presence(activity=newact,)
        await inter.send(f"Presence set to `{type} {name}` ")

    @dev.sub_command()
    async def joinvc(self,inter:disnake.CmdInter,channel:disnake.VoiceChannel):
        vc:disnake.VoiceClient = await channel.connect()
        await inter.send("Connected!",view=VcView(
            timeout=None,
            vc=vc,
            inter=inter,
            bot=self.bot
            )
        )
        pass



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