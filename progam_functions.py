import json, os, logging, time, re, string, os
from datetime import datetime

converters = {
"50 free": (0.860, 0.871),
"100 free": (0.863, 0.874),
"200 free": (0.865, 0.874),
"400 free": (1.105, 1.112),
"800 free": (1.105, 1.120),
"1500 free": (0.965, 0.975),
"100 free": (0.868, 0.877),
"200 free": (0.866, 0.881),
"100 back": (0.835, 0.853),
"200 back": (0.849, 0.857),
"100 breast": (0.856, 0.870),
"200 breast": (0.858, 0.878),
"200 IM": (0.857, 0.867),
"400 IM": (0.865, 0.876)
}

def checkfiles(guild):
    if os.path.isdir(f'./guildfiles/{guild}.json') == True:
        return
    else:
        joinguild(guild)
        return

def joinguild(guild):
    if os.path.exists(f'./guildfiles/{guild}.json') == True:
        return
    else:
        with open(f'./guildfiles/{guild}.json', 'w') as f:
            f.write(f"{{}}")

def check_event(event):
  _input = input()
  if event in converters:
    x = converters.get(event)
    return x
  else:
    return None


def lcm(time, event, gender):
    x = check_event(event)
    if x != None:
        pass

    return newtime

def scy(time, event, gender):
    x = check_event(event)
    if x == None:
        return 
    if gender.lower == 'm':
        y = 0
    elif gender.lower == 'f':
        y = 1


    if gender != 0 or 1:
        pass

    return newtime















