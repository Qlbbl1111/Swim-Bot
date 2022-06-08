import json, os, logging, time, re, string, os
import datetime
from time import gmtime
from time import strftime
from decimal import getcontext, Decimal

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

def seconds(time):
    time = time
    #change time to seconds
    try:
        date_time = datetime.datetime.strptime(time, "%M:%S.%f")
        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
        return a_timedelta.total_seconds()
    except:
        try:
            date_time = datetime.datetime.strptime(time, "%S.%f")
            a_timedelta = date_time - datetime.datetime(1900, 1, 1)
            return a_timedelta.total_seconds()
        except:
            return None

def swimtime(time):
    #change time back to 00:00.00
    newtime = divmod(time, 60)
    t = newtime[0]
    t2 = newtime[1]
    _min = int(t)
    t2 = round(t2, 2)
    sec = zeros(t2)
    if _min == 0:
        return f"{sec}"
    else:
        return f"{_min:02d}:{sec}"

def gettime(course, time, distance, stroke):
    if course.lower() == "lcm":
        course = 0
    elif course.lower() == "scy":
        course = 1
    else:
        return "Error"

    if course == 1 and distance == "500" or course == 1 and distance == "1000" or course == 1 and distance == "1650" or course == 0 and distance == "400" or course == 0 and distance == "800" or course == 0 and distance == "1500":
        return "Mistake"

    x = seconds(time)

    converters = {
"fly": {
    "50": [(x-0.7)/1.11, x*1.11+0.7],

    "100": [(x-1.4)/1.11, x*1.11+1.4],

    "200": [(x-2.8)/1.11, x*1.11+2.6]
    },

"back": {
    "50": [(x-0.6)/1.11, x*1.11+0.6],

    "100": [(x-1.2)/1.11, x*1.11+1.2],

    "200": [(x-2.4)/1.11, x*1.11+2.4]
    },

"breast": {
    "50": [(x-1.0)/1.11, x*1.11+1.0],

    "100": [(x-2.0)/1.11, x*1.11+2.0],

    "200": [(x-4.0)/1.11, x*1.11+4.0]
    },

"free": {
    "50": [(x-0.8)/1.11, x*1.11+0.8],

    "100": [(x-1.6)/1.11, x*1.11+1.6],

    "200": [(x-3.2)/1.11, x*1.11+3.2],

    "400": [x/0.8925, x*0.8925],
    "500": [x/0.8925, x*0.8925],

    "800": [x/0.8925, x*0.8925],
    "1000": [x/0.8925, x*0.8925],

    "1500": [x/1.02, x*1.02],
    "1650": [x/1.02, x*1.02]
    },

"im": {
    "200": [(x-3.2)/1.11, x*1.11+3.2],

    "400": [(x-6.4)/1.11, x*1.11+6.4]
    },
}
    try:
        newtime = converters.get(stroke.lower()).get(distance.lower())[course]
    except:
        return "Error"

    return swimtime(newtime)

def getpace(goal, distance, split, practice):
    x = seconds(goal)

    pacecalc = {
    "100": {
        "25": x/4,
        "50": x/2,
        "100": x/1
        },
    "200": {
        "25": x/8,
        "50": x/4,
        "100": x/2
        },
    "400": {
        "25": x/16,
        "50": x/8,
        "100": x/4
        },
    "500": {
        "25": x/20,
        "50": x/10,
        "100": x/5
        }
    }
    practicepacecalc = {
    "100": {
        "25": (x+2)/4,
        "50": (x+2)/2,
        "100": (x+2)/1
        },
    "200": {
        "25": (x+2)/8,
        "50": (x+2)/4,
        "100": (x+2)/2
        },
    "400": {
        "25": (x+2)/16,
        "50": (x+2)/8,
        "100": (x+2)/4
        },
    "500": {
        "25": (x+2)/20,
        "50": (x+2)/10,
        "100": (x+2)/5
        }
    }

    try:
        if practice.lower() == "n":
            pace = pacecalc.get(distance.lower()).get(split.lower())
        if practice.lower() == "y":
            pace = practicepacecalc.get(distance.lower()).get(split.lower())
        return swimtime(pace)
    except:
        return "Error"




