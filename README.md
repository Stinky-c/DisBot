# dis bot

----

A bot created using Disnake with various togglable modules

The github is a mirror of a local repo

----

## TODO

- [ ] [pytube](https://github.com/pytube/pytube) -> [youtube_dl](https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl) - Maybe
    - download and delete after sending/using?
    - `download.py`

- [ ] Music player
    - skip function
    - continued play

----

## requirements

- Python 3.10 - other versions untested
    - installed requirements.txt

- [ffmpeg](https://ffmpeg.org/)
    - path placed in `definitions.py`
    - to disable add `music` to disabled cogs

- `.env` file in the root directory containing
    - Discord bot token named `DISBOTTOKEN1`

- `config.toml`
    - change guild ids to guilds you wish to register commands
    - change owner ids to people you wish be able to use debug commands
    - [optional]
        - logging
            - paths
            - encoding
            - formatting
            - toggle send to user or channel
        - random cow
            - min & max chance
        - quotes
            - quotes that are sent upon mention or command usage
            - quotes sent upon the bot stopping
        - status
            - the status the bot sets upon booting
        - cogs
            - enabled dev cogs
            - disabled main cogs

----

## Docs

- installing latest patch using pip

    - ```pip install -U git+https://github.com/DisnakeDev/disnake#egg=disnake[speed,voice]```

- [fixing pytube streams bug](https://stackoverflow.com/questions/68945080/pytube-exceptions-regexmatcherror-get-throttling-function-name-could-not-find/71903013#71903013)

    - ```pip install -U git+https://github.com/kinshuk-h/pytube@72075dddb2153bde89a8de9eb8def91d41da3655```

- Disnake docs
    - [guide](https://guide.disnake.dev/)
    - [docs](https://docs.disnake.dev/en/latest/api.html)

----

### ideas

- WIP market game
    - TODO
        - find database
            - Document?
            - improvise with sqlite3
        - do math to determine the market to ensure there is some difference without user interaction

- Downloaders
    - supported
        - youtube   - needs a better way, could stream the audio and video together
        - reddit    - stream audio and video to be able to download from website
    - TODO
        - [TikTok](https://taksave.com/)
        - [Instagram](https://igram.io)
            - [post1](https://www.instagram.com/p/CdYi-2arvAV/)
            - [post2](https://www.instagram.com/p/CdYejSVMrXq/)
            - [post3](https://www.instagram.com/reel/CcqWe5cqnKh/)

- [ ] database drivers
    - [sqlite3 DB driver](https://github.com/plasticityai/supersqlite)
    - [mongo DBdriver](https://github.com/mongodb/motor)
    - [async sqlite3 driver](https://aiosqlite.omnilib.dev/en/latest/)

- [ ] voice chat based chatbot
    - joins a vc and converse with a user
    - only allow 1 person to talk
        - require a stage channel?
    - convert speech to text and process it
    - resulting processed text played back using tts
    - a lot of processing power needed

- [ ] website
    - provide tools from bot?
    - admin panel for bot?
    - frameworks
        - django?
            - needs ground up rebuild
            - probably incompatible
        - flask?
            - needs ground up rebuild
            - microservice
