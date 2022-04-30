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
          "name": f"{prefix}convert",
          "value": "Used to convert times."
        },
        {
          "name": f"{prefix}test",
          "value": "Used to test the bot."
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
 

#Time converter
@bot.command()
async def convert(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send('All is good here!')

@convert.error
async def convert_error(ctx, error):
    await ctx.send('Somthing went wrong') 

#RUN
if __name__ == "__main__":
    bot.run(os.environ.get("KEY"))