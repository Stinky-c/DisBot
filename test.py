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


video = "C:\Projects\DisBot\page2.html" # https://www.reddit.com/r/ProgrammerHumor/comments/uiw8wh/
gif = "C:\Projects\DisBot\page.html"    # https://www.reddit.com/r/standardissuecat/comments/ui22c7/
image = "C:\Projects\DisBot\page3.html" # https://www.reddit.com/r/softwaregore/comments/uj0mdr/
error = "C:\Projects\DisBot\page4.html" # https://redditsave.com/info?url=
all = [
    "C:\Projects\DisBot\page.html",
    "C:\Projects\DisBot\page2.html",
    "C:\Projects\DisBot\page3.html",
]
with open(video) as f:
    soup = BeautifulSoup(f,"html.parser")
    download = soup.find("div", {"class": "download-info"}).find("a") if not soup.find("div", {"class": "alert alert-danger"}) else None


videodet = [
    ("download_sound_video","video"),
    ("download_ireddit_gif","gif"),
    ("download_generic","generic")
    ]

next = download.attrs["onclick"]
for erm in videodet:
    if erm[0] in next:
        break
print(erm[1])
# print(download)
# res = req.get(download)
# print(res.headers)
# pass