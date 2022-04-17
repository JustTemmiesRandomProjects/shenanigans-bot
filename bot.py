import discord
from discord import Intents
from discord.ext import commands, tasks
import json

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



for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
  
  
@tasks.loop(minutes=15)
async def change_status_task():
  with open("data/leaderboard.json", "r") as f:
        data = json.load(f)
        
  a = 0
  pin_list = []
        
  for x in data:
      pin_list.append({int(data[x]['pins']), int(x)})
  
  for x in pin_list:
      pin_list[a] = sorted(pin_list[a], reverse=False)
      a += 1
      
  pin_list = sorted(pin_list, reverse=True)
  
  status = pin_list[0][1]
  await bot.change_presence(status=discord.Status.idle,
  activity=discord.Activity(type=discord.ActivityType.watching, 
  name=(status)))


bot.run((TOKEN), bot=True, reconnect=True)