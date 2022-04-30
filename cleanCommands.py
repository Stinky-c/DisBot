from datetime import datetime
import discord
import os
from dotenv import load_dotenv
load_dotenv()
bot = discord.Bot(debug_guilds=[771385874688245770,851204839605927946])
@bot.event
async def on_ready():
    # bot.add_view(View())
    print(f"{bot.user}; {datetime.now()}")
    await bot.sync_commands()
    bot.close()
bot.run(os.environ["DISBOTTOKEN1"])