import aiohttp
import time
import re
from bs4 import BeautifulSoup
import requests as req
from urllib import parse
import base64 as b64

link2 = "https://www.reddit.com/r/maybemaybemaybe/comments/ui4ocr/maybe_maybe_maybe/?utm_source=share&utm_medium=web2x&context=3"
urlreg = re.compile(r"https://www\.reddit\.com/r/.*")
if re.match(urlreg,link2):
    link = "https://redditsave.com/info?url="+parse.quote(link2)
    soup = BeautifulSoup(req.get(link).content, 'html.parser')
    download = soup.find("div", {"class": "download-info"}).find("a") if not soup.find("div", {"class": "alert alert-danger"}) else None

'''
video = ".\page2.html"  # https://www.reddit.com/r/ProgrammerHumor/comments/uiw8wh/
gif = ".\page.html"     # https://www.reddit.com/r/standardissuecat/comments/ui22c7/
image = ".\page3.html"  # https://www.reddit.com/r/softwaregore/comments/uj0mdr/
videoS = ".\page5.html" # https://www.reddit.com/r/PeopleFuckingDying/comments/uivfwf/
videoNS = ".\page6.html"# https://www.reddit.com/r/GamePhysics/comments/uj5y0k/
text = ".\page7.html"   # https://www.reddit.com/r/HomeNetworking/comments/tgboo8/
error = ".\page4.html"  # https://redditsave.com/info?url=
all = [
    video,
    gif,
    image,
    videoS,
    videoNS,
    text,
    error,
]'''


videodet = [
    ("download_sound_video","video-sound"),
    ("download_ireddit_gif","gif"),
    ("download_vreddit_no_sound","video-no-sound"),
    ("download_generic","generic"),
    ]
if download:
    next = download.attrs["onclick"]
    nexthref = download.get("href")
    for erm in videodet:
        if erm[0] in next:
            break
    pass
    match erm[1]:
        case "video-sound":
            with open(f"G:\projects\disBot2\{str(time.time()).split('.')[0]}-sound.mp4","wb") as f:
                f.write(req.get(nexthref).content)
        case "video-no-sound":
            with open(f"G:\projects\disBot2\{str(time.time()).split('.')[0]}-no-sound.mp4","wb") as f:
                f.write(req.get(nexthref).content)
        case "gif":
            nextcurrent = b64.b64decode(nexthref.replace("/d/","")).decode()
            print(nextcurrent,erm[1])
        case "generic":
            print("not supported")
        case _:
            print("error")

