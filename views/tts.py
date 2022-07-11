import logging
import disnake
from disnake.ext import commands
from googletrans import Translator
import gtts as gt
import os
import shutil
import uuid
from definitions import FFMPEG_PATH


class TTSReqeuestModal(disnake.ui.Modal):
    def __init__(self, custom_id):
        self.timeout = None
        components = [
            disnake.ui.TextInput(
                label="Sentence",
                custom_id="sentence",
                style=disnake.TextInputStyle.paragraph,
                max_length=3000,
                required=True,
            ),
            disnake.ui.TextInput(
                label="Language - Supported languages only",
                custom_id="lang",
                style=disnake.TextInputStyle.short,
                max_length=2,
                required=True,
                value="en",
            ),
        ]
        super().__init__(
            title="Request Sentence",
            custom_id=custom_id,
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.defer()
        await inter.send(
            f"Saying \n```{inter.text_values.get('sentence',None)}```", delete_after=5.0
        )

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
        await inter.send(f"An error occurred!\n```{error}```")

    async def on_timeout(self):
        pass


class TTSView(disnake.ui.View):
    def __init__(
        self,
        *,
        vc: disnake.VoiceClient,
        inter: disnake.CmdInter,
        bot: commands.Bot,
        logger: logging.Logger,
    ):
        super().__init__(
            timeout=None,
        )
        self.custom_id = str(uuid.uuid4())
        self.vc = vc
        self.inter = inter
        self.bot = bot
        self.oginter = inter
        self.logger = logger

        self.univSupLangs = {
            "af": "afrikaans",
            "ar": "arabic",
            "bg": "bulgarian",
            "bn": "bengali",
            "bs": "bosnian",
            "ca": "catalan",
            "hr": "croatian",
            "cs": "czech",
            "da": "danish",
            "nl": "dutch",
            "en": "english",
            "eo": "esperanto",
            "et": "estonian",
            "tl": "filipino",
            "fi": "finnish",
            "fr": "french",
            "de": "german",
            "el": "greek",
            "gu": "gujarati",
            "iw": "hebrew",
            "hi": "hindi",
            "hu": "hungarian",
            "is": "icelandic",
            "id": "indonesian",
            "it": "italian",
            "ja": "japanese",
            "jw": "javanese",
            "kn": "kannada",
            "km": "khmer",
            "ko": "korean",
            "la": "latin",
            "lv": "latvian",
            "mk": "macedonian",
            "ms": "malay",
            "ml": "malayalam",
            "mr": "marathi",
            "my": "myanmar (burmese)",
            "ne": "nepali",
            "no": "norwegian",
            "pl": "polish",
            "pt": "portuguese",
            "ro": "romanian",
            "ru": "russian",
            "sr": "serbian",
            "si": "sinhala",
            "sk": "slovak",
            "es": "spanish",
            "su": "sundanese",
            "sw": "swahili",
            "sv": "swedish",
            "ta": "tamil",
            "te": "telugu",
            "th": "thai",
            "tr": "turkish",
            "uk": "ukrainian",
            "ur": "urdu",
            "vi": "vietnamese",
            "cy": "welsh",
        }
        self.supLang = gt.lang.tts_langs()
        self.supLangF = "Please be exact while using the keys, else it will not work\n```key | Full Name\n    |\n af | afrikaans\n ar | arabic\n bg | bulgarian\n bn | bengali\n bs | bosnian\n ca | catalan\n hr | croatian\n cs | czech\n da | danish\n nl | dutch\n en | english\n eo | esperanto\n et | estonian\n tl | filipino\n fi | finnish\n fr | french\n de | german\n el | greek\n gu | gujarati\n iw | hebrew\n hi | hindi\n hu | hungarian\n is | icelandic\n id | indonesian\n it | italian\n ja | japanese\n jw | javanese\n kn | kannada\n km | khmer\n ko | korean\n la | latin\n lv | latvian\n mk | macedonian\n ms | malay\n ml | malayalam\n mr | marathi\n my | myanmar (burmese)\n ne | nepali\n no | norwegian\n pl | polish\n pt | portuguese\n ro | romanian\n ru | russian\n sr | serbian\n si | sinhala\n sk | slovak\n es | spanish\n su | sundanese\n sw | swahili\n sv | swedish\n ta | tamil\n te | telugu\n th | thai\n tr | turkish\n uk | ukrainian\n ur | urdu\n vi | vietnamese\n cy | welsh```"
        self.trans = Translator()
        self.path = "temp/" + self.custom_id
        os.mkdir(self.path)

    @disnake.ui.button(label="English", style=disnake.ButtonStyle.green)
    async def engl(self, button: disnake.Button, inter: disnake.CmdInter):
        modid = str(uuid.uuid4())
        await inter.response.send_modal(modal=TTSReqeuestModal(modid))
        mod_inter: disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == modid and i.author.id == inter.author.id,
            timeout=300,
        )

        p = f"{self.path}/{uuid.uuid4()}.mp4"

        val = mod_inter.text_values.get("lang")
        if val in self.supLang:
            lang = val
        else:
            lang = "en"

        sentence = mod_inter.text_values.get("sentence")

        gt.gTTS(sentence, lang=lang, tld="com").save(p)
        ac = disnake.FFmpegOpusAudio(p, executable=FFMPEG_PATH)
        self.vc.play(ac)
        self.logger.info(
            f"{inter.author.name} said {sentence}:{lang} in {inter.channel.name}:{inter.guild.id}"
        )  # log here
        pass

    @disnake.ui.button(label="Auto", style=disnake.ButtonStyle.green)
    async def autot(self, button: disnake.Button, inter: disnake.CmdInter):
        modid = str(uuid.uuid4())
        await inter.response.send_modal(modal=TTSReqeuestModal(modid))
        mod_inter: disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == modid and i.author.id == inter.author.id,
            timeout=300,
        )

        sentence = mod_inter.text_values.get("sentence", None)
        p = f"{self.path}/{uuid.uuid4()}.mp4"

        val = mod_inter.text_values.get("lang")
        lang = val if val in self.supLang else "en"
        translated = self.trans.translate(sentence, dest=lang)
        gt.gTTS(translated.text, lang=translated.dest, tld="com").save(p)
        ac = disnake.FFmpegOpusAudio(p, executable=FFMPEG_PATH)
        self.vc.play(ac)
        self.logger.info(
            f"{inter.author.name} said {sentence}:{lang} in {inter.channel.name}:{inter.guild.id}"
        )  # log here
        pass

    @disnake.ui.button(label="Leave", style=disnake.ButtonStyle.red)
    async def leaveCallback(self, button: disnake.Button, inter: disnake.CmdInter):
        await self.vc.disconnect()
        await inter.send("left!", delete_after=5.0)
        await self.inter.delete_original_message(delay=5.0)
        shutil.rmtree(self.path)
        self.stop()

    @disnake.ui.button(label="Languages", style=disnake.ButtonStyle.blurple)
    async def languages(self, button: disnake.Button, inter: disnake.CmdInter):
        await inter.send(self.supLangF, ephemeral=True)

    async def on_timeout(self):
        self.vc.disconnect(force=True)
        self.oginter.edit_original_message("Thats all folks.\nCall me if you need me")

    async def on_error(self, error: Exception, inter: disnake.CmdInter, *args) -> None:
        await self.inter.send("An error occured")
        self.logger.info(error)  # Log here
