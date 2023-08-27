import discord
from discord import Intents
from discord.ext import commands, tasks
import glob
import asyncio

import os
from dotenv import load_dotenv
load_dotenv("DIS_TOKEN.env")
TOKEN = os.getenv("KEY")

bot = commands.Bot(
  command_prefix = "--",
  intents=Intents.all()
)

@bot.event
async def on_ready():
  
  change_status_task.start()

  guild_count = 0
  for guild in bot.guilds:
      print(f"- {guild.id}) (name: {guild.name})")
      guild_count = guild_count + 1
    
  print(f"{bot.user} is in " + str(guild_count) + " guild(s).")


  
@tasks.loop(minutes=15)
async def change_status_task():
  await bot.change_presence(status=discord.Status.idle,
  activity=discord.Activity(type=discord.ActivityType.watching, 
  name=("beavers")))


async def setup(bot):
    # loads cogs
    for filename in glob.iglob("./cogs/**", recursive=True):
        if filename.endswith('.py'):
            filename = filename[2:].replace("/", ".") # goes from "./cogs/economy.py" to "cogs.economy.py"
            await bot.load_extension(f'{filename[:-3]}') # removes the ".py" from the end of the filename, to make it into cogs.economy
    

async def main():
    async with bot:
        await setup(bot)
        await bot.start(TOKEN)

asyncio.run(main())
