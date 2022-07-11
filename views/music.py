import disnake
from disnake.ext import commands
from definitions import *
from datetime import datetime
import random as rnd
from pytube import YouTube
import shutil
import asyncio


class LinkView(disnake.ui.View):
    """
    Takes list of tuples to add buttons addcordingly
    `[("Label","Link"),("label2","link2")]`
    or a singular tuple following the same scheme
    `("label","link")`
    """

    def __init__(self, link: tuple = None, links: list = None):
        super().__init__()
        if link:
            self.add_item(
                disnake.ui.Button(
                    label=link[0], url=link[1], style=disnake.ButtonStyle.link
                )
            )
        if links:
            for i in links:
                self.add_item(
                    disnake.ui.Button(
                        label=i[0], url=i[1], style=disnake.ButtonStyle.link
                    )
                )


# music player
class SongRequestModal(disnake.ui.Modal):
    def __init__(self, custom_id):
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
        await inter.send(
            f"'{inter.text_values.get('link',None)}' has been added!", delete_after=5.0
        )

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
        await inter.send(f"An error occurred!\n```{error}```")

    async def on_timeout(
        self,
    ):
        pass


# Welcome to callback hell
class VcView(disnake.ui.View):
    # add some verbose to this
    def __init__(
        self,
        *,
        timeout: float = None,
        vc: disnake.VoiceClient,
        inter: disnake.CmdInter,
        bot: commands.Bot,
    ):
        super().__init__(timeout=timeout)
        self.vc = vc
        self.inter = inter
        self.path = os.path.join(TEMP_PATH, self.id)
        self.bot = bot
        self.oginter = inter
        self.vc.pause()
        self.playlist: dict = {
            "status": vc.is_paused(),
            "playing": None,
            "queue": [
                # debug songs
                # "https://www.youtube.com/watch?v=gh4LKacwiKE",
                # "https://www.youtube.com/watch?v=ARSFhILy-2I",
                # "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ],
        }

    async def poll(self, error=None, *args, **kwargs) -> str:
        message: disnake.InteractionMessage = await self.oginter.original_message()
        musicEmbed = {
            "title": "Music Player",
            "color": disnake.Color.random().value,
            "timestamp": datetime.now().isoformat(),
            "fields": [],
        }
        musicEmbed["fields"].append(
            {"name": "Status", "value": str(self.playlist["status"]), "inline": "false"}
        )
        musicEmbed["fields"].append(
            {"name": "Playing", "value": self.playlist["playing"], "inline": "false"}
        ) if self.playlist["playing"] is not None else ""
        musicEmbed["fields"].append(
            {"name": "Queue", "value": "next up:", "inline": "false"}
        )
        for link in self.playlist["queue"]:
            musicEmbed["fields"].append(
                {"name": "Link", "value": link, "inline": "false"}
            )
        await message.edit(embed=disnake.Embed.from_dict(musicEmbed))
        # updates the message list
        # use a dict and make a function to return it as a usable string
        pass

    @disnake.ui.button(label="Toggle Pause", style=disnake.ButtonStyle.green)
    async def pauseCallback(self, button: disnake.Button, inter: disnake.CmdInter):
        if not self.vc.is_playing():
            await inter.send("Not currently playing music", delete_after=5.0)
            return

        status = self.vc.is_paused()
        match status:
            case True:
                self.vc.resume()
                self.playlist["status"] = True
                await inter.send(f"{inter.author.name} has unpaused", delete_after=5.0)
                button.label = "Pause"

            case False:
                self.vc.pause()
                self.playlist["status"] = False
                await inter.send(f"{inter.author.name} has paused", delete_after=5.0)
                button.label = "Pause"
        await self.poll()

    @disnake.ui.button(label="Append Song", style=disnake.ButtonStyle.green)
    async def songCallback(self, button: disnake.Button, inter: disnake.CmdInter):
        # TODO capture input and validate it here
        modid = str(rnd.random())
        await inter.response.send_modal(modal=SongRequestModal(modid))
        mod_inter: disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == modid and i.author.id == inter.author.id,
            timeout=300,
        )
        self.playlist["queue"].append(mod_inter.text_values.get("link", None))
        # poll the songs and append to the list
        # find a way to allow people to reorder the list
        # or skip the current song
        await self.poll()
        pass

    async def play(self, error=None):
        try:

            link = self.playlist["queue"].pop(0)
            pathS = YouTube(link).streams.get_audio_only().download(self.path)
            src = disnake.FFmpegOpusAudio(pathS, executable=FFMPEG_PATH)
            self.playlist["playing"] = link
            self.vc.play(src, after=(await self.play))
        except IndexError:
            return
        except Exception as e:
            raise e
        pass

    @disnake.ui.button(label="Play", style=disnake.ButtonStyle.green)
    async def playCallback(self, button: disnake.Button, inter: disnake.CmdInter):
        await inter.response.defer()
        if self.vc.is_playing():
            await inter.send("The bot is currently playing", delete_after=5.0)
            return

        await inter.send("Playing now", delete_after=5.0)

        # await self.play()

        link = self.playlist["queue"].pop(0)
        pathS = YouTube(link).streams.get_audio_only().download(self.path)
        src = disnake.FFmpegOpusAudio(pathS, executable=FFMPEG_PATH)
        self.playlist["playing"] = link
        await inter.send("Playing now", delete_after=5.0)
        self.vc.play(
            src,
        )
        await self.poll()

    @disnake.ui.button(
        label="Skip",
    )
    async def skipCallback(self, button: disnake.Button, inter: disnake.CmdInter):
        self.vc.stop()
        await inter.send(f"{inter.author.name} has skipped!", delete_after=5.0)
        await self.poll()

    @disnake.ui.button(label="Leave", style=disnake.ButtonStyle.red)
    async def leaveCallback(self, button: disnake.Button, inter: disnake.CmdInter):
        await self.vc.disconnect()
        await inter.response.send_message("left!", delete_after=5.0)
        await self.inter.delete_original_message(delay=5.0)
        shutil.rmtree(self.path) if os.path.isdir(self.path) else ""
        await asyncio.sleep(5.5)
        self.stop()
