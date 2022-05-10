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
          "value": "Used to bring up this menu."
        },
        {
          "name": f"{prefix}test",
          "value": "Used to test the bot."
        },
        {
          "name": f"{prefix}convert",
          "value": f"Used to convert times.\nFormat is `{prefix}convert course[scy/lcm] time[00:00.00] event`"
        }
      ]
    }
  ))


#Test the bot
@bot.command()
async def test(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send('All is good here!')

@test.error
async def test_error(ctx, error):
    await ctx.send('Somthing went wrong')
 
#Test the bot
@bot.command()
async def events(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Events that can be converted:",
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
      "name": "LCM or SCY:",
      "value":  '''
                - 50 free
                - 100 free
                - 200 free
                - 400 free
                - 800 free
                - 1500 free
                - 100 fly
                - 200 fly
                - 100 back
                - 200 back
                - 100 breast
                - 200 breast
                - 200 IM
                - 400 IM

                '''
        }
      ]
    }
  ))


#Time converter
@bot.command()
async def convert(ctx, course, time, *event):
    checkfiles(ctx.guild.id)
    event = event[0]+ ' ' + event[1]

    if course.lower() == 'lcm':
        newtime = lcm(time, event)
        if newtime != None:
            await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Converted LCM to SCY",
      "color": 0,
      "description": f"LCM: {time}\n SCY: {newtime}",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {
        "text": "If you think this is wrong please report it.",

      },
        "fields": [
        {
      "name": "LCM:",
      "value": f"{time}",
        },
        {
      "name": "SCY:",
      "value": f"{newtime}",
        }
      ]
    }
))
        else:
            pass

    elif course.lower() == 'scy':
        newtime = scy(time, event)
        if newtime != None:
            await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Converted SCY to LCM",
      "color": 0,
      "description": "",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {
        "text": "If you think this is wrong please report it.",

      },
      "fields": [
        {
      "name": "SCY:",
      "value": f"{time}",
        },
        {
      "name": "LCM:",
      "value": f"{newtime}",
        }
      ]
    }
))
        else:
            pass
    else:
        newtime = None

    if newtime == None:
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Error: BadArgument",
      "color": 0,
      "description": f"Command format is: \n`{prefix}convert course[scy/lcm] time[00:00.00] event`",
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
    if isinstance(error, commands.BadArgument):
        await ctx.send('Somthing went wrong')




#RUN
if __name__ == "__main__":
    bot.run(os.environ.get("KEY"))