import discord
from discord.ext import commands, tasks
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, cooldown, BucketType
import random
from datetime import datetime
import json

IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_leaderboard_timer.start()
  

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        author_id = payload.data['author']['id']
        #author = self.bot.get_user(payload.data['author']['id'])
        message_id = payload.data['id']
        is_pinned = payload.data['pinned']
        
        change = 0
        
        with open("data/pinned_messages.json", "r") as f:
            data = json.load(f)
        
        
        for x in data['messages']:
            if int(x) == int(message_id):
                return

        if is_pinned:
            data['messages'].append(int(message_id))
            with open("data/pinned_messages.json", "w") as f:
                json.dump(data, f)
            
            change = 1
 
            await self.open_db(author_id)
            #await self.get_data()
            await self.update_data(author_id, change)
            
    
    @commands.command()
    async def leaderboard(self, ctx):
        await self.update_leaderboard()
            

    @tasks.loop(seconds=300)
    async def update_leaderboard_timer(self):
        try:
            await self.update_leaderboard()
        except Exception as e:
            print("error " + str(e))
            
    
    @commands.Cog.listener()
    async def update_leaderboard(self):
        channel = self.bot.get_channel(628212961218920479) # the message's channel
        msg_id = 965067100571959387 # the message's id
        
        info = ""
        n = 1
        a = 0
        
        data = await self.get_data()
        pin_list = []
        
        for x in data:
            pin_list.append({int(data[x]['pins']), int(x)})
        
        for x in pin_list:
            pin_list[a] = sorted(pin_list[a], reverse=False)
            a += 1
            
        pin_list = sorted(pin_list, reverse=True)
        
        for input in pin_list:
            pin_string = "pin"
            person = await self.bot.fetch_user(input[1])
            pins = input[0]
            if pins != 1:
                pin_string = "pins"
            
            if n % 10 == 1:
                placement = "st"
            elif n % 10 == 2:
                placement = "nd"
            elif n % 10 == 3:
                placement = "rd"
            else:
                placement = "th"
            
            info += (str(n) + f"{placement} - " + person.display_name + " with " + str(pins) + f" {pin_string}\n")
            
            n += 1
        
        leaderboard = await channel.fetch_message(msg_id)
        await leaderboard.edit(content=
                f"**Leaderboard:**\n\n{info}")
        

    
    @commands.Cog.listener()
    async def open_db(self, author):

        data = await self.get_data()

        if str(author) in data:
            return False

        else:
            data[str(author)] = {}
            data[str(author)]["pins"] = 0

        with open("data/leaderboard.json", "w") as f:
            json.dump(data, f)
        
        return True


    
    @commands.Cog.listener()
    async def get_data(self):
        with open("data/leaderboard.json", "r") as f:
            data = json.load(f)
        
        return data


    @commands.Cog.listener()
    async def update_data(self, user, change = 0):
        users = await self.get_data()

        users[str(user)]["pins"] += change

        with open("data/leaderboard.json", "w") as f:
            json.dump(users, f)
    
def setup(bot):
    bot.add_cog(events(bot))