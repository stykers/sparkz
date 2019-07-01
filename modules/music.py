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


async def trydel(context, quiet=True):
    try:
        await context.delete()
    except discord.Forbidden:
        if quiet:
            await context.send("I lack the permission to delete messages.")
        else:
            pass
    except AttributeError:
        try:
            await context.message.delete()
        except discord.Forbidden:
            if quiet:
                await context.send("I lack the permission to delete messages.")
            else:
                pass
        except AttributeError:
            print(f"Attribute error! Please report this in an issue.")


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')


class Music(commands.Cog):
    """ Music related features. """

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Music(bot))
