import time
import json
import discord
import timeago as timesince

from collections import namedtuple
from io import BytesIO


def get(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Invalid usage.")
    except FileNotFoundError:
        raise FileNotFoundError("No such file or directory.")


def timetext(name):
    return f"{name}_{int(time.time())}.txt"