import discord
from discord import Intents
from discord.ext import commands, tasks

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

  guild_count = 0
  for guild in bot.guilds:
      print(f"- {guild.id}) (name: {guild.name})")
      guild_count = guild_count + 1
    
  print(f"{bot.user} is in " + str(guild_count) + " guild(s).")



for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


bot.run((TOKEN), bot=True, reconnect=True)