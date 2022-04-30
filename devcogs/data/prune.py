import json
import random
import os
import time
import shutil
import re
optioncount = 15
maxfiles = 1
if True:
    try:
        shutil.rmtree(f"{os.path.dirname(__file__)}/random/")
    except:
        pass
    os.mkdir(f"{os.path.dirname(__file__)}/random/")

for _ in range(maxfiles):
    # load
    with open(f"{os.path.dirname(__file__)}/foaas.json") as f:
        howfuck:dict = json.load(f)
    # prune
    for i in range(len(howfuck),optioncount,-1):
        howfuck.pop(random.randint(0,i)-1)

    # update fields
    for i in howfuck:
        i["url"] = re.sub(":from","{from_}",i["url"])
        i["url"] = re.sub(":name","{name}",i["url"])
    # write
    with open(f"{os.path.dirname(__file__)}/random/{str(time.time()).split('.')[1]}.json","w+") as f:
        json.dump(howfuck,f,indent=4)
    print(_)