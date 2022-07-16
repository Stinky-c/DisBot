import io
import disnake
from disnake.ext import commands
import logging
import qrcode as qrc

from typing import Tuple
from helper.qr import full as emebedHelp

from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *
from qrcode.image.styledpil import *
from qrcode.constants import *
from qrcode.image.svg import *

# TODO:
# resizing
# random things to say when sending
# this file: to use pil then default to pymaging on import error


class QuickResponseCodeCog(commands.Cog):
    # keep function dict in one line
    # fmt: off
    def _colorTupleHelper(self,fullcolorstr:str)-> Tuple[int,int,int]:
        colorlist=fullcolorstr.split(",")
        colortuple = ()
        for colorstr in colorlist:
            colortuple+= (int(colorstr),)
        return tuple(colortuple)

    moddrawer = {"Square Data": SquareModuleDrawer,"Gapped Square Data": GappedSquareModuleDrawer,"Circle Data": CircleModuleDrawer,"Rounded Data": RoundedModuleDrawer,"Vertical Bars Data": VerticalBarsDrawer,"Horizontal Bars Data": HorizontalBarsDrawer,}
    colormasks = {"SolidFillColorMask":SolidFillColorMask,"RadialGradiantColorMask":RadialGradiantColorMask,"SquareGradiantColorMask":SquareGradiantColorMask,"HorizontalGradiantColorMask":HorizontalGradiantColorMask,"VerticalGradiantColorMask":VerticalGradiantColorMask,"ImageColorMask":ImageColorMask}
    errorCorrectionLevel={"7%":ERROR_CORRECT_L,"15%":ERROR_CORRECT_M,"25%":ERROR_CORRECT_Q,"30%":ERROR_CORRECT_H,}

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.loggerl2 = logging.getLogger("disnakecommands.QR.cmd")

        self.colormasks={"SolidFillColorMask":SolidFillColorMask,"RadialGradiantColorMask":RadialGradiantColorMask,"SquareGradiantColorMask":SquareGradiantColorMask,"HorizontalGradiantColorMask":HorizontalGradiantColorMask,"VerticalGradiantColorMask":VerticalGradiantColorMask,"ImageColorMask":ImageColorMask}
        self.moddrawer = {"Square Data": SquareModuleDrawer,"Gapped Square Data": GappedSquareModuleDrawer,"Circle Data": CircleModuleDrawer,"Rounded Data": RoundedModuleDrawer,"Vertical Bars Data": VerticalBarsDrawer,"Horizontal Bars Data": HorizontalBarsDrawer,}
        self.errorCorrectionLevel={"7%":ERROR_CORRECT_L,"15%":ERROR_CORRECT_M,"25%":ERROR_CORRECT_Q,"30%":ERROR_CORRECT_H,}

    # fmt: on
    @commands.slash_command(name="qr")
    async def qrG(self, inter):
        self.loggerl2.info(f"{inter.user.name} ran a command")  # sub command logger
        pass

    async def cog_load(self):
        # async functions here
        pass

    @qrG.sub_command(description="Creates a code from minimal options")
    async def auto(
        self,
        inter: disnake.CmdInter,
        data: str = None,
        file: disnake.Attachment = None,
    ):
        buf = io.BytesIO()
        if data:
            img = qrc.make(data)
        elif file:
            img = qrc.make(file)
        else:
            await inter.send("Data or file is required")
            return
        img.save(buf)
        buf.seek(0)
        await inter.send(
            "I have automatically created a code for that data",
            file=disnake.File(buf, "QuickResponse.png"),
        )

    @qrG.sub_command(description="Creates stylized a code in the PNG format")
    async def stylized(
        self,
        inter: disnake.CmdInter,
        data: str = None,
        file: disnake.Attachment = None,
        style: str = commands.Param(
            choices=list(moddrawer.keys()),
            description="Style for the data contained in the code",
        ),
        colorfg: str = commands.Param(
            description="Comma seperated RGB value for the foreground",
            conv=_colorTupleHelper,
        ),
        colorbg: str = commands.Param(
            description="Comma seperated RGB value for the background",
            conv=_colorTupleHelper,
        ),
        error_correction: str = commands.Param(
            default="15%", choices=list(errorCorrectionLevel.keys())
        ),
    ):
        print(colorbg)
        print(colorfg)
        # TODO: Colorized ones
        qrstyle = qrc.QRCode(
            error_correction=self.errorCorrectionLevel[error_correction]
        )
        if data:
            qrstyle.add_data(data)
        elif file:
            qrstyle.add_data(file)
        else:
            await inter.send("Data or file is required")
            return
        qrstyle.make(True)
        await inter.response.defer()
        img = qrstyle.make_image(
            image_factory=StyledPilImage,
            module_drawer=self.moddrawer[style](),
            color_mask=SolidFillColorMask(front_color=colorfg, back_color=colorbg),
        )
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        await inter.send(
            "I have automatically created a stylized code for that data",
            file=disnake.File(buf, "StylizedQuickResponse.png"),
        )
        pass

    @qrG.sub_command(name="ascii", description="Creates a code in the ASCII format")
    async def asciiC(
        self,
        inter: disnake.CmdInter,
        data: str = None,
        file: disnake.Attachment = None,
        as_file: bool = False,
    ):
        qrascii = qrc.QRCode(error_correction=ERROR_CORRECT_H)
        if data:
            qrascii.add_data(data)
        elif file:
            qrascii.add_data(file)
        else:
            await inter.send("Data or file is required")
            return
        buf = io.StringIO()
        qrascii.print_ascii(buf)
        buf.seek(0)
        a = buf.read()
        if as_file:
            buf2 = io.BytesIO(a.encode("utf-8"))
            await inter.send(
                f"I have automatically created a code for that data",
                file=disnake.File(buf2, "QuickResponse.txt"),
            )
            return
        else:
            await inter.send(
                f"I have automatically created a code for that data\n```\n{a}\n```"
            )
            return

    @qrG.sub_command(name="svg", description="Creates a code in the SVG format")
    async def svgS(
        self, inter: disnake.CmdInter, data: str = None, file: disnake.Attachment = None,
        error_correction: str = commands.Param(
            default="15%", choices=list(errorCorrectionLevel.keys())
        ),
    ):
        qrsvg = qrc.QRCode(
            error_correction=self.errorCorrectionLevel[error_correction],
            image_factory=SvgFillImage,
        )
        if data:
            qrsvg.add_data(data)
        elif file:
            qrsvg.add_data(file)
        else:
            await inter.send("Data or file is required")
            return

        qrsvg.make(True)
        img = qrsvg.make_image()
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        await inter.send(
            f"I have automatically created a code for that data",
            file=disnake.File(buf, "QuickResponse.svg"),
        )
    @qrG.sub_command(description="The help command")
    async def help(self,inter:disnake.CmdInter,command:str = commands.Param(choices=list(emebedHelp.keys()))):
        await inter.send(embed=emebedHelp[command])


def setup(bot):
    logging.getLogger("disnakecommands.QR").info(f"{__name__} is online")  # init logger
    bot.add_cog(QuickResponseCodeCog(bot), override=True)
