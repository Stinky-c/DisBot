#/usr/bin/python3.7

import time
import json
import discord
import requests as re
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class MyClient(discord.Client):

    global cleanUp
    def cleanUp(toClean,badChar) -> str: 

        '''
        returns the first part of cleaned string removing everything after a bad char.
        else returns the first string 
        '''
        
        try:
            return toClean.split(badChar)[0]
        except IndexError:
             return toClean
    '''
    MyClient is a rude bot who i made some how
    '''

    async def on_ready(self):
        print(f"Logged on as {self.user} at {datetime.today().strftime('%Y-%m-%d-%H:%M:%S')} ")

    async def on_message(self, message):
        

        if message.author.id == self.user.id: # its me!
            # print(f"Hey, thats me!\n{time.time()}")
            return

        prefixes = ["w!","weather"]
        if message.content.lower().split(" ")[0] not in prefixes: # Ignore message if its not starting with the prefix
            return

        try: # ignores a missing command or errors for some other reason
            message.content.split(" ")[1]
        except Exception as e:
            await message.channel.send("You either missed a command or the bot has failed!\n use `w! help` for the command list")
            return



        if message.content.split(" ")[1].lower() == "help": # Help command
            await message.channel.send(prompts.helpMessage)
            return
            
        if message.content.split(" ")[1].lower() == "city": # returns a city
            try:
                place = message.content.split(" ")[2]
                place = cleanUp(place,"?")
                link = f"https://wttr.in/{place}?T?0?q"
            except Exception as e:
                await message.channel.send("Be sure to specify a city!")
                # print(e)
                return

            res = re.get(link)
            await message.channel.send(f"```\n{res.content.decode()}\n```")

        if message.content.split(" ")[1].lower() == "json": # returns a city in json format
            try:
                place = message.content.split(" ")[2]
                place = cleanUp(place,"?")
                link = f"https://wttr.in/{place}?format=j2"
            except Exception as e:
                await message.channel.send("Be sure to specify a city!")
                # print(e)
                return

            res = re.get(link)
            resJson = res.json()

            await message.channel.send(f"```\n{resJson}\n```")
            await message.channel.send(f"The Length of that json was {len(str(resJson))}")


        if message.content.split(" ")[1].lower() == "alt":
            try:
                try:
                    place = message.content.split(" ")[2]
                    flags = message.content.split(" ")[3]
                except:
                    await message.channel.send("Missing 1 or more flags \nExample: `weather alt Florida ?q?T?0`")
                    return
                link = f"https://wttr.in/{place}{flags}"
                res = re.get(link)
                if not len(str(res.content.decode())) > 2000:
                    await message.channel.send(f"the link: <{link}>\n```\n{res.content.decode()}\n```")
                else:
                    await message.channel.send(f"The payload was `{len(str(res.content.decode()))}` characters in length and could not be sent :sob: \nBut the link is still here! {link}")
            except Exception as e:
                print(e)

        if message.content.split(" ")[1].lower() == "jsonq": # json query
            try:
                place = message.content.split(" ")[2]
                place = cleanUp(place,"?")
                obj = message.content.split(" ")[3]
                obj = obj.split("+")
                link = f"https://wttr.in/{place}?format=j1"
                try:
                    res = re.get(link)
                    resJson = res.json()
                    await message.channel.send(f"The value of the field was `{resJson[obj[0]][obj[1]][obj[2]]}`")
                except:
                    await message.channel.send("Be sure to include all flags\nFlag 3 keyword are split using a `+`")

            except Exception as e:
                await message.channel.send("Be sure to include all flags")
                print(e)
                return

            res = re.get(link)
            resJson = res.json()

            await message.channel.send(f"```\n{resJson}\n```")
            await message.channel.send(f"The Length of that json was {len(str(resJson))}")
 

        if message.content.split(" ")[1].lower() == "ping!": # ping! pong!
            await message.channel.send(f"{message.content.split(' ')[0]} Pong!")
        if message.content.split(" ")[1].lower() == "test":
            await message.channel.send(f"{message.content.split(' ')}")



class things:

    '''
    Contains misc large messages and such
    '''

    def __init__(self):
        self.helpMessage = f'''```\nThe available commands are: \n\
        'City': Gets the city specified, be sure to use a + instead of a space\n
        'help': Shows this message, hello there!\n
        'json': to get json data \n 
        'alt': allows for the creation of the links 
        \nsome extra encoding: https://wttr.in/:help\n```'''
        self.importantMessage = \
            f'''```
this is an important message
            ```''' 

prompts = things() 
client = MyClient()
client.run(os.environ["DISBOTTOKEN3"])
