import re
from bs4 import BeautifulSoup
import requests as req
from urllib import parse

'''
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
]
for i in all:
    print()
    with open(i) as f:
        soup = BeautifulSoup(f,"html.parser")
        download = soup.find("div", {"class": "download-info"}).find("a") if not soup.find("div", {"class": "alert alert-danger"}) else None


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
                print(nexthref,erm[1])
            case "video-no-sound":
                print(nexthref,erm[1])
            case "gif":
                print(nexthref,erm[1])
            case "generic":
                print(nexthref,erm[1])
            case _:
                print("error",nexthref,erm[1])

# print(download)
# res = req.get(download)
# print(res.headers)
# pass