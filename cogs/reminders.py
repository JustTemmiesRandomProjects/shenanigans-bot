from discord import Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import time

async def str_replacer(initial_string, ch, replacing_character, occurrence):

    # breaking a string into it's
    # every single character in list
    lst1 = list(initial_string)
    lst2 = list(ch)

    # List to store the indexes in which
    # it is replaced with the
    # replacing_character
    lst3 = []

    # Loop to find the Nth occurrence of
    # given characters in the string
    for i in lst2:
        if lst1.count(i) >= occurrence:
            count = 0
            for j in range(0, len(initial_string)):
                if i == lst1[j]:
                    count += 1
                    if count == occurrence:
                        lst3.append(j)

    for i in lst3:
        # Replacing that particular index
        # with the requested character
        lst1[i] = replacing_character

    val = "".join(lst1)

    return val


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="remindme",
        aliases=["remind", "reminder"],
        brief='reminds you of something\na!remindme god damn it tell her i like beavers in 1 day 2 hours 30 min\nyou can use "day(s), d", "hour(s), h(r)", "minute(s), m(in)", "second(s), s(ec)"',
    )
    @cooldown(5, 10, BucketType.user)
    async def reminder_command(self, ctx, *, reminder):
        seconds = 0
        arraything = reminder.split(" in ")

        timing = arraything[len(arraything) - 1]
        reminder.join(arraything)

        ch = " "
        occurrence = 2
        replacing_character = ","

        # calls funny function from rust library that does some wacky shit
        timing = await str_replacer(timing, ch, replacing_character, occurrence)

        timing = timing.split(",")
        for i in timing:
            duration = float(i.split(" ")[0])
            if "day" in i:
                seconds += duration * 86400
            elif "hour" in i:
                seconds += duration * 3600
            elif "minute" in i:
                seconds += duration * 60
            elif "second" in i:
                seconds += duration

            else:
                single_letters = i.split(" ")[1].replace(" ", "")
                if single_letters == "d":
                    seconds += duration * 86400
                elif single_letters == "h" or single_letters == "hr":
                    seconds += duration * 3600
                elif single_letters == "m" or single_letters == "min":
                    seconds += duration * 60
                elif single_letters == "s" or single_letters == "sec":
                    seconds += duration

                else:
                    return await ctx.send(f"{timing} is an invalid time format, please use a valid time format - use `{ctx.prefix}help remindme` for more info")

        if seconds < 30:
            return await ctx.send(f"please set a time greater than 30 seconds")

        if seconds > 31536000:
            return await ctx.send(f"please set a time less than 1 year")

        sendtime = round(time.time() + seconds)
        embed = Embed(title=reminder, description=f"i will remind you <t:{sendtime}:R>", color=ctx.author.colour)
        embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        with open("data/reminders.json", "r") as f:
            data = json.load(f)

        if not str(ctx.author.id) in data:
            data[str(ctx.author.id)] = {}

        data[str(ctx.author.id)][sendtime] = reminder

        with open("data/reminders.json", "w") as f:
            json.dump(data, f)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(reminder(bot))
