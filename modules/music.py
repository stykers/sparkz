import discord
import asyncio
import os
import youtube_dl
import glob
import logging

from discord.ext import commands
from util import list
from util import music


useaira = 0
logvids = False
skipsreq = 3
ffbefopts = '-nostdin'
ffopts = '-vn -reconnect 1'
ytdl_npm = youtube_dl.YoutubeDL(list.ytdl_noplaylist)
ytdl = youtube_dl.YoutubeDL(list.ytdl_format_options)
ytdl_aria = youtube_dl.YoutubeDL(list.ytdl_aria)


class Music(commands.Cog):
    """ Music related features. """

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Music(bot))
