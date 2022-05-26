import disnake
from disnake.ext import commands
import logging
from datetime import datetime
from views import LinkView


class UserCog(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command()
    async def userfunc(self, inter: disnake.CmdInter):
        self.loggerl2.info(f"{inter.user.name} ran a command")  # sub command logger

        pass

    @commands.user_command(name="View Song")
    async def spotifysong(self, inter: disnake.CmdInter, user: disnake.Member):
        if not any(isinstance(x, disnake.Spotify) for x in list(user.activities)):
            await inter.send("That person is not listening to spotify", ephemeral=True)
            return

        spot = next(
            (x for x in list(user.activities) if isinstance(x, disnake.Spotify)), None
        )
        embed_dict = {
            "type": "image",
            "title": spot.title,
            "description": ", ".join(spot.artists),
            "color": spot.color.value,
            "image": {"url": spot.album_cover_url},
        }
        await inter.send(
            embed=disnake.Embed.from_dict(embed_dict),
            view=LinkView(link=("Track Link", spot.track_url)),
        )
        self.loggerl2.info(
            f"{user.name} is listening to '{spot.title}' by '{spot.artists}' on spotify\nLink{spot.track_url}"
        )

    @commands.user_command()
    async def avatar(self, inter: disnake.CmdInter, user: disnake.Member):
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
                {
                    "name": "Account creation date",
                    "value": disnake.utils.snowflake_time(user.id).strftime(
                        "%a %b %d at %I:%M:%S UTC"
                    ),
                    "inline": "false",
                },
            ],
            "image": {"url": user.display_avatar.url},
            "footer": {
                "icon_url": "https://raw.githubusercontent.com/Stinky-c/Stinky-c/main/svg/it-just-works-somehow.png"
            },
        }

        await inter.response.send_message(embed=disnake.Embed.from_dict(embed_dict))


def setup(bot):
    logging.getLogger("disnakecommands.user").info(
        f"{__name__} is online"
    )  # init logger
    bot.add_cog(UserCog(bot), override=True)
