# dis bot

----
A bot created using

----

## Docs

- installing latest patch using pip
    - `git+https://github.com/DisnakeDev/disnake#egg=disnake[speed,voice]`

- [fixing pytube streams bug](https://stackoverflow.com/questions/68945080/pytube-exceptions-regexmatcherror-get-throttling-function-name-could-not-find/71903013#71903013)

- disanke docs
    - [guide](https://guide.disnake.dev/)
    - [docs](https://docs.disnake.dev/en/latest/api.html)

----

### ideas

- WIP market game
    - TODO
        - find database
            - Document?
            - improvise with sqlite3
        - do math to determine the market to ensure there is some differnce without user interation

- downloaders
    - supported
        - youtube   - needs a better way, could stream the audio and video together
        - reddit    - stream audio and video to be able to download from website
    - TODO
        - [tiktok](https://taksave.com/)
        - [instagram](https://igram.io)
            - [insta post1](https://www.instagram.com/p/CdYi-2arvAV/)
            - [insta post2](https://www.instagram.com/p/CdYejSVMrXq/)
            - [insta post3](https://www.instagram.com/reel/CcqWe5cqnKh/)

- [ ] database drivers
    - [sqlite3 DB driver](https://github.com/plasticityai/supersqlite)
    - [mongo DBdriver](https://github.com/mongodb/motor)
    - [async sqlite3 driver](https://aiosqlite.omnilib.dev/en/latest/)

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
