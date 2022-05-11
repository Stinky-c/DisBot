import disnake
from disnake.ext import commands
import logging
import re
import base64 as b64
from pytube import YouTube
import tempfile
from bs4 import BeautifulSoup
import requests as req
from urllib import parse 
import time
import io
import aiohttp

class DownloadCog(commands.Cog):

    def __init__(self, bot:commands.InteractionBot):
        self.bot = bot
        self.loggerl2 = logging.getLogger("disnakecommands.download.cmd")
        self.urlreg = re.compile(r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))") 
        self.redditreg = re.compile(r"https://www\.reddit\.com/r/.*")
        self.aiohttp = aiohttp.ClientSession()


    @commands.slash_command()
    async def download(self,inter):
        self.loggerl2.info(f"{inter.user.name} ran a command") # sub command logger

        pass
# cmd: youtubedownload
# TODO write sort algorithm for file size or give options
# IDEA add filesize to pytube stream object
    @download.sub_command(description="Downloads a YouTube video from a link returning the best video under 8mb")
    async def youtube(self,inter:disnake.CmdInter,link:str):
        """Downloads a YouTube video at the highest quality possible under 8mb

        Args:
            link (str): Must be a link
        """
        try:
            if not re.match(self.urlreg,link):
                await inter.send("Please provide a valid link\n Example:`https://www.youtube.com/watch?v=dQw4w9WgXcQ` or `https://youtu.be/dQw4w9WgXcQ`")
                return
            yt = YouTube(link)
            await inter.response.defer()
            vids = yt.streams.order_by("resolution").desc().filter(type="video",progressive=True,mime_type="video/mp4",)
            if len(vids) == 0:
                self.loggerl2.info(f"'{yt.title}' cannot be downloaded due to invaild filters")
                await inter.send(f"'{yt.title}' cannot be downloaded due to invaild filters")
                return

            for vid in vids:
                if vid.filesize_approx <= 8388608:
                    break

            if vid.filesize_approx >= 8388608:
                self.loggerl2.info(f"'{yt.title}' cannot be downloaded due to its length and quality\nTry a smaller, or shorter video")
                await inter.send(f"'{yt.title}' cannot be downloaded due to its length and quality")
                return

            with tempfile.TemporaryDirectory() as td:
                self.loggerl2.info(f"'{inter.user.name}' downloaded '{yt.title}'; size: {round(vid.filesize_approx/1024,5)}kb\ndata: '{vid}'")
                await inter.send(file=disnake.File(vid.download(td)))
                return
        except Exception as e:
            self.loggerl2.error(e)
            self.loggerl2.error(f"the downloading of '{yt.title}' has errored")
            await inter.send("Something went ***really*** wrong\nPlease contact Bucky")
# cmd : redditdownload
# TODO fix it
    @download.sub_command()
    async def reddit(self,inter:disnake.CmdInter,link:str):
        """Downloads a Reddit video as a file, or a Gif as a link

        Args:
            link (str): Must be a link
        """
        if not re.match(self.redditreg,link):
            await inter.send("Please provide a valid link\n Example:`https://www.reddit.com/r/blurrypicturesofcats/comments/uigcmv/blurry_picture_of_a_cat/` or `https://www.reddit.com/r/blurrypicturesofcats/comments/uigcmv/`")
            return

        fullLink = "https://redditsave.com/info?url="+parse.quote(link)
        soup = BeautifulSoup(req.get(fullLink).content, 'html.parser')
        downloadA = soup.find("div", {"class": "download-info"}).find("a") if not soup.find("div", {"class": "alert alert-danger"}) else None
        if downloadA is None:
            await inter.send("This link is invalid")
            return
        videodet = [
        ("download_sound_video","video-sound"),         # supported
        ("download_ireddit_gif","gif"),                 # supported
        ("download_vreddit_no_sound","video-no-sound"), # supported
        ("download_generic","generic"),                 # not supported
        ]
        await inter.response.defer()
        if downloadA:
            next = downloadA.attrs["onclick"]
            nexthref = downloadA.get("href")
            for video in videodet:
                if video[0] in next:
                    break

            match video[1]:
                case "video-sound":
                    async with self.aiohttp.get(nexthref) as res:
                        if len(await res.read()) >= 8388608:
                            await inter.send("The file is too large")
                            return
                        await inter.send(file=disnake.File(io.BytesIO(await res.read()),f"{str(time.time()).split('.')[0]}-sound.mp4"))
                    self.loggerl2.info(f"sound video: {inter.author} downloaded '{link}'")
                    return
                case "video-no-sound":
                    async with self.aiohttp.get(nexthref) as res:
                        if len(await res.read()) >= 8388608:
                            await inter.send("The file is too large")
                            return
                        await inter.send(file=disnake.File(io.BytesIO(await res.read()),f"{str(time.time()).split('.')[0]}-no-sound.mp4"))
                    self.loggerl2.info(f"no sound video: {inter.author} downloaded '{link}'")
                    return
                case "gif":
                    nextcurrent = b64.b64decode(nexthref.replace("/d/","")).decode()
                    await inter.send(nextcurrent)
                    self.loggerl2.info(f"gif: {inter.author} downloaded '{link}'")
                    return
                case "generic":
                    await inter.send("This post type is not supported")
                    self.loggerl2.info(f"'{link}' is not supported")
                    return
                case _:
                    await inter.send("This post has errored")
                    self.loggerl2.error(f"'{link}' errored for an unknown reason")
                    return
'''
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
'''
def setup(bot): 
    logging.getLogger("disnakecommands.download").info(f"{__name__} is online") # init logger
    bot.add_cog(DownloadCog(bot),override=True) 