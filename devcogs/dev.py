import asyncio
from datetime import datetime
import disnake
import aiohttp
from disnake.ext import commands
import requests as req
import random as rnd
from pytube import YouTube
import json
import re
import logging
import shutil
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
class SongRequestModal(disnake.ui.Modal):
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
            title="Append Song",
            custom_id=custom_id,
            components=components,
        )
    async def callback(self, inter: disnake.ModalInteraction):
        await inter.send(f"'{inter.text_values.get('link',None)}' has been added!",delete_after=5.0)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
        await inter.send(f"An error occurred!\n```{error}```")
    async def on_timeout(self,):
        pass

class VcView(disnake.ui.View):
    # add some verbose to this
    def __init__(self, *, timeout:float=None,vc:disnake.VoiceClient,inter:disnake.CmdInter,bot:commands.Bot):
        super().__init__(timeout=timeout)
        self.vc = vc
        self.inter = inter
        self.path = os.path.join(TEMP_PATH,self.id)
        self.bot = bot
        self.oginter = inter
        self.vc.pause()
        self.playlist:dict = {
            "status": vc.is_paused(),
            "playing":None,
            "queue":[
                # debug songs
                # "https://www.youtube.com/watch?v=gh4LKacwiKE",
                # "https://www.youtube.com/watch?v=ARSFhILy-2I",
                # "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ],
        }

    async def poll(self,error=None,*args, **kwargs) -> str:
        message:disnake.InteractionMessage = await self.oginter.original_message()
        musicEmbed = {
            "title": "Music Player",
            "color": disnake.Color.random().value,
            "timestamp": datetime.now().isoformat(),
            "fields": [
            ],
        }
        musicEmbed["fields"].append({"name": "Status", "value": str(self.playlist["status"]), "inline": "false"})
        musicEmbed["fields"].append({"name": "Playing", "value": self.playlist["playing"], "inline": "false"}) if self.playlist["playing"] is not None else ""
        musicEmbed["fields"].append({"name": "Queue", "value": "next up:", "inline": "false"})
        for link in self.playlist["queue"]:
            musicEmbed["fields"].append({"name": "Link", "value": link, "inline": "false"})
        await message.edit(embed=disnake.Embed.from_dict(musicEmbed))
        # updates the message list
        # use a dict and make a function to return it as a usable string
        pass

    @disnake.ui.button(label="Toggle Pause",style=disnake.ButtonStyle.green)
    async def pauseCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        if not self.vc.is_playing():
            await inter.send("Not currently playing music",delete_after=5.0)
            return

        status = self.vc.is_paused()
        match status:
            case True:
                self.vc.resume()
                self.playlist["status"] = True
                await inter.send(f"{inter.author.name} has unpaused",delete_after=5.0)
                button.label = "Pause"

            case False:
                self.vc.pause()
                self.playlist["status"] = False
                await inter.send(f"{inter.author.name} has paused",delete_after=5.0)
                button.label = "Pause"
        await self.poll()

    @disnake.ui.button(label="Append Song",style=disnake.ButtonStyle.green)
    async def songCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        # TODO capture input and validate it here
        modid = str(rnd.random())
        await inter.response.send_modal(modal=SongRequestModal(modid))
        mod_inter:disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check= lambda i: i.custom_id == modid and i.author.id == inter.author.id,
            timeout=300
        )
        self.playlist["queue"].append(mod_inter.text_values.get("link",None))
        # poll the songs and append to the list
        # find a way to allow people to reorder the list
        # or skip the current song
        await self.poll()
        pass


    async def play(self,error=None):
        try:

            link = self.playlist["queue"].pop(0)
            pathS = YouTube(link).streams.get_audio_only().download(self.path)
            src = disnake.FFmpegOpusAudio(
                pathS,
                executable=FFMPEG_PATH
                )
            self.playlist["playing"] = link
            self.vc.play(src,after=(await self.play))
        except IndexError:
            return
        except Exception as e:
            raise e
        pass

    @disnake.ui.button(label="Play",style=disnake.ButtonStyle.green)
    async def playCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        await inter.response.defer()
        if self.vc.is_playing():
            await inter.send("The bot is currently playing",delete_after=5.0)
            return

        await inter.send("Playing now",delete_after=5.0)

        # await self.play()

        link = self.playlist["queue"].pop(0)
        pathS = YouTube(link).streams.get_audio_only().download(self.path)
        src = disnake.FFmpegOpusAudio(
            pathS,
            executable=FFMPEG_PATH
            )
        self.playlist["playing"] = link
        await inter.send("Playing now",delete_after=5.0)
        self.vc.play(src,)
        await self.poll()


    @disnake.ui.button(label="Skip",)
    async def skipCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        self.vc.stop()
        await inter.send(f"{inter.author.name} has skipped!",delete_after=5.0)
        await self.poll()

    @disnake.ui.button(label="Leave",style=disnake.ButtonStyle.red)
    async def leaveCallback(self,button:disnake.Button,inter:disnake.CmdInter):
        await self.vc.disconnect()
        await inter.response.send_message("left!",delete_after=5.0)
        await self.inter.delete_original_message(delay=5.0)
        shutil.rmtree(self.path) if os.path.isdir(self.path) else ""
        await asyncio.sleep(5.5)
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

    # @dev.sub_command()
    # async def testembed(self,inter:disnake.CmdInter):
    #     embed_dict = {
    #         "title": "Music Player",
    #         "color": disnake.Color.random().value, #done
    #         "timestamp": datetime.now().isoformat(),
    #         "fields": [
    #             {"name": "Link", "value": "link", "inline": "false"},
    #         ],
    #     }
    #     await inter.send(embed=disnake.Embed.from_dict(embed_dict))

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