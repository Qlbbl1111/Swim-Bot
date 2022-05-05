import json, os, logging, time, re, string, os
import datetime
from time import gmtime
from time import strftime
from decimal import getcontext, Decimal

converters = {
"50 free": 0.871,
"100 free": 0.874,
"200 free": 0.874,
"400 free": 1.112,
"800 free": 1.120,
"1500 free": 0.975,
"100 free": 0.877,
"200 free": 0.881,
"100 back": 0.853,
"200 back": 0.857,
"100 breast": 0.870,
"200 breast": 0.878,
"200 im": 0.867,
"400 im": 0.876
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


def zeros(number):
    x = str(number)
    if len(x) == 1: 
        y = x.zfill(2)
    elif len(x) == 3 and x[1] == '.': 
        y = x.zfill(4)
    elif x[1] == '.' and len(x) != 3:
        y = x.zfill(5)
    elif x[1] == '.' and len(x) == 3:
        y = x.zfill(4)
    else:
        y = x
    return y


def gettime(time, course, converter):
    #change time to seconds
    date_time = datetime.datetime.strptime(time, "%M:%S.%f")
    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()

    #convert
    if course == 'scy':
        newtime = seconds/converter
    if course == 'lcm':
        newtime = seconds*converter

    newtime = round(newtime, 2)
    print(newtime)
    #change time back to 00:00.00
    newtime = divmod(newtime, 60)
    t = newtime[0]
    t2 = newtime[1]
    _min = int(t)
    t2 = round(t2, 2)
    sec = zeros(t2)

    return f"{_min:02d}:{sec}"


def check_event(event):
    _event = event.lower()

    if _event in converters:
        x = converters.get(event)
        return x
    else:
        return None


def lcm(time, event):
    x = check_event(event)

    if x == None:
        return None
    else:
        return gettime(time, 'lcm', x)


def scy(time, event):
    x = check_event(event)

    if x == None:
        return None
    else:
        return gettime(time, 'scy', x)
    


