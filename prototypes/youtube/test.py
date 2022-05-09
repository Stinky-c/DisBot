'''    
@dev.sub_command()
async def listvideo(self,inter:disnake.CmdInter,link:str):
    if not re.match(self.urlreg,link):
        await inter.send("Please provide a valid link\n Example:`https://www.youtube.com/watch?v=dQw4w9WgXcQ` or `https://youtu.be/dQw4w9WgXcQ`")
        return
    yt = YouTube(link)
    vids = yt.streams
    await inter.send("printed to console")
    print(vids)

@dev.sub_command()
async def getvideo(self,inter:disnake.CmdInter,link:str,itag:int):
    if not re.match(self.urlreg,link):
        await inter.send("Please provide a valid link\n Example:`https://www.youtube.com/watch?v=dQw4w9WgXcQ` or `https://youtu.be/dQw4w9WgXcQ`")
        return
    yt = YouTube(link)
    vid = yt.streams.get_by_itag(itag)
    if vid.filesize >= 8388608:
        self.loggerl2.info(f"'{inter.user.name}' downloaded '{yt.title}'; size: {round(vid.filesize/1024,5)}kb\ndata: '{vid}'")
        await inter.send("Failed")
        return
    await inter.response.defer()
    with tempfile.TemporaryDirectory() as td:
        self.loggerl2.info(f"'{inter.user.name}' downloaded '{yt.title}'; size: {round(vid.filesize/1024,5)}kb\ndata: '{vid}'")
        await inter.send(file=disnake.File(vid.download(td)))
        return
            '''