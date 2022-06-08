from dotenv import load_dotenv
import discord, json, os, logging, time, re, string, os.path
from discord.ext import commands, tasks
from progam_functions import *

#Program Variables
dir = os.path.dirname(__file__)

#Program Functions
load_dotenv(os.path.join(dir, ".env"))

if os.path.isdir('./guildfiles') != True:
    os.mkdir(os.path.join('./', 'guildfiles'))      
else:
    pass

# Discord Variables
activity = discord.Activity(type=discord.ActivityType.listening, name="~~help")
author_id = "892999941146963969"
prefix = '~~'

# Bot info
bot = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    activity=activity,
    status=discord.Status.online
)
bot.author_id = author_id 
bot.remove_command("help") #For custom help command

# Logger
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

#bot startup
@bot.event
async def on_ready():  # When the bot is ready
    print(f"{bot.user} Started.")


#EVENTS
#creates guild settings
@bot.event
async def on_guild_join(guild):
    joinguild(guild.id)
    return


#Message respond event
@bot.listen('on_message')
async def on_message(message):
    #set vars
    checkfiles(message.guild.id)
    pass


#COMMANDS
#help command
@bot.command()
async def help(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Swim Bot Help",
      "color": 0,
      "description": "This is a list of commands and their descriptions.",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
          "name": f"{prefix}help",
          "value": f"Used to bring up this menu."
        },
        {
          "name": f"{prefix}test",
          "value": f"Used to test the bot.\nCommand format is:\n`{prefix} optional_agrs'"
        },
        {
          "name": f"{prefix}convert",
          "value": f"Used to convert LCM to and from SCY.\nCommand format is:\n`{prefix}convert course[scy/lcm] time[00:00.00] distance[100] stroke[free]`"
        },
          {
          "name": f"{prefix}pace",
          "value": f"Used to get goal pace calculations for your swims.\nCommand format is:\n`{prefix}pace goal_time[2:00.00] race_distance[200] split[50] (optional)practice[y/n]`"
        }
      ]
    }
  ))


#Test the bot
@bot.command()
async def test(ctx, *arg):
    checkfiles(ctx.guild.id)
    await ctx.send(f'All is good here!\n{arg}')

@test.error
async def test_error(ctx, error):
    await ctx.send(f"Error: {error}")
 
#All the available events
@bot.command()
async def events(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "",
      "color": 0,
      "description": "",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
      "name": "Events that can be converted:",
      "value":  '''
                **Freestyle:**
                - 50 Free
                - 100 Free
                - 200 Free
                - 500 Free <=> 400 Free
                - 1000 Free <=> 800 Free
                - 1650 Free <=> 1500 Free

                **Butterfly:**
                - 50 Fly
                - 100 Fly
                - 200 Fly

                **Backstroke:**
                - 50 Back
                - 100 Back
                - 200 Back

                **Breaststroke:**
                - 50 Breast
                - 100 Breast
                - 200 Breast

                **Individual Medley:**
                - 200 IM
                - 400 IM

                '''
        }
      ]
    }
  ))


#Time converter
@bot.command()
async def convert(ctx, course, time, distance, stroke):
    checkfiles(ctx.guild.id)
    newtime = gettime(course, time, distance, stroke)
    if course.lower() == 'lcm':
        course = ["LCM", "SCY"]
    elif course.lower() == 'scy':
        course = ["SCY", "LCM"]

    if newtime != "Error" and newtime != "Mistake":
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": f"Converted {course[0]} to {course[1]}",
      "color": 0,
      "description": f"**Event:** {distance} {stroke}",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {
        "text": "",

      },
        "fields": [
        {
      "name": f"{course[0]}:",
      "value": f"{time}",
        },
        {
      "name": f"{course[1]}:",
      "value": f"{newtime}",
        }
      ]
    }
))
    elif newtime == "Error":
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Error: BadArgument",
      "color": 0,
      "description": f"Command format is: \n`{prefix}convert course[scy/lcm] time[00:00.00] distance[100] stroke[free]`",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
                    {
                        "name": "To view available events run:",
                        "value": f"{prefix}events"
                    }
      ]
    }
  ))
    elif newtime == "Mistake":
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Error: Invalid Conversion",
      "color": 0,
      "description": f"{distance} {stroke} can't be converted to {course[0]}.\nTry converting it to {course[1]}.",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
                    {
                        "name": "To view available events run:",
                        "value": f"{prefix}events"
                    }
      ]
    }
  ))

@convert.error
async def convert_error(ctx, error):
    await ctx.send(f"Error: {error}")


#Pace calculator
@bot.command()
async def pace(ctx, goal, distance, split, practice="n"):
    checkfiles(ctx.guild.id)
    pace ="pace"
    pace = getpace(goal, distance, split, practice)
    if pace != "Error" and practice.lower() == "n":
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": f"Here's your {split} pace to go {goal}:",
      "color": 0,
      "description": f"{pace}",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }
  ))
    elif pace != "Error" and practice.lower() == "y":
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": f"Here's your {split} pace to go {goal} in practice:",
      "color": 0,
      "description": f"{pace}",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {
        "text": "Practice mode takes into account the dive by adding 2 seconds to your goal time before calculating.",

      },
      "fields": []
    }
  ))  
    elif pace == "Error":
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Error: Invalid Distance or Split",
      "color": 0,
      "description": f"""
      **Valid Distances:**
      - 100
      - 200
      - 400
      - 500

      **Valid Splits:**
      - 25
      - 50
      - 100
      """,
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }
  ))

@pace.error
async def pace_error(ctx, error):
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": f"Error: {error}",
      "color": 0,
      "description": f"Command format is:\n`{prefix}pace goal_time[2:00.00] race_distance[200] split[50] (optional)practice[y/n]`",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {
        "text": "Practice mode takes into account the dive by adding 2 seconds to your goal time before calculating.",

      },
      "fields": []
    }
  ))

#View the bot credits.
@bot.command()
async def credits(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Credits:",
      "color": 0,
      "description": "",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
      "name": "Bot Author",
      "value":  '''
        **Quinn Burke**
        My stuff can be found here:
        [Github](https://github.com/Stanback/)
        [Twitter](https://twitter.com/Qlbbl1111)
        Qlbbl#1111

                '''
        },
        {
      "name": "A big thanks to Brian Stanback for the conversion formulas.",
      "value":  '''
        His GitHub can be found [here](https://github.com/Stanback/).

                '''
        }
      ]
    }
  ))

#RUN
if __name__ == "__main__":
    bot.run(os.environ.get("KEY"))