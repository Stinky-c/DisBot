import re
from bs4 import BeautifulSoup
import requests as req
from urllib import parse
link2 = "https://www.reddit.com/r/maybemaybemaybe/comments/ui4ocr/maybe_maybe_maybe/?utm_source=share&utm_medium=web2x&context=3"
urlreg = re.compile(r"https://www\.reddit\.com/r/.*")
if re.match(urlreg,link2):
    link = "https://redditsave.com/info?url="+parse.quote(link2)
    soup = BeautifulSoup(req.get(link).content, 'html.parser')
    download = soup.find("div", {"class": "download-info"}).find("a").get("href") if not soup.find("div", {"class": "alert alert-danger"}) else None
print(download)
res = req.get(download)
print(res.headers)
pass
# print("small" if len(req.get(download).content) <= 8388608 else "large")