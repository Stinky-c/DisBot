import sqlite3
import disnake
from disnake.ext import commands
import logging
# import aiosqlite as aiodb
import os

class MarketCog(commands.Cog):

    def __init__(self, bot:commands.InteractionBot):
        self.loggerl2 = logging.getLogger("disnakecommands.market.cmd")
        self.bot = bot
        self.con = sqlite3.connect(os.path.dirname(__file__)+"/market.db") # database connection
        # self.connecter = await aiodb.connect(os.path.dirname(__file__)+"/mark.db") 

    def checkUser(self,id:int):
        """Checks if the user is in the database

        Args:
            id (int): discord user id

        Returns:
            bool: Returns True if the user exists else returns flase
        """
        cur= self.con.cursor()
        cur.execute(f"SELECT id FROM users WHERE id=?",(id,))
        dbid = cur.fetchone()
        if dbid is not None and dbid is id:
            return True
        else:
            return False


    @commands.slash_command()
    async def mark(self,inter:disnake.CmdInter):
        self.loggerl2.info(f"{inter.user.name} ran a command") # sub command logger
        pass


    @mark.sub_command()
    async def start(self,inter:disnake.CmdInter):
        cur = self.con.cursor()
        if not self.checkUser(inter.author.id):
            await inter.send("you are already registered")
            return

        self.con.execute(f"INSERT INTO users VALUES (?,?,?)",(inter.author.id,100,inter.author.name))
        await inter.send("you are now registered")
        self.con.commit()

    @mark.sub_command()
    async def read(self,inter:disnake.CmdInter):
        await inter.send("AAA")
        cursor = self.con.execute("SELECT * FROM stocks;")
        for stock in cursor:
            print(stock)
        pass


    @mark.sub_command()
    async def close(self,inter:disnake.CmdInter):
        self.con.commit()
        self.con.close()
        print("closed")
        await inter.send("AAA")

        pass

def setup(bot): 
    logging.getLogger("disnakecommands.market").info(f"{__name__} is online") # init logger
    bot.add_cog(MarketCog(bot),override=True) 