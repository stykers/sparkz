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
ytdl_npl = youtube_dl.YoutubeDL(list.ytdl_noplaylist)
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

    @classmethod
    async def from_url(cls, url, *, loop=None, aria=False):
        loop = loop or asyncio.get_event_loop()
        if aria:
            data = await loop.run_in_executor(None, ytdl_aria.extract_info, url)
        else:
            data = await loop.run_in_executor(None, ytdl_npl.extract_info, url)
        if 'entries' in data:
            data = data['entries'][0]
        filename = (ytdl_npl.prepare_filename(data))
        return cls(discord.FFmpegPCMAudio(filename, before_options=ffbefopts, options=ffopts), data=data)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.requester = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False
        return not self.voice.is_playing()

    @property
    def player(self):
        return self.current.player


class Music(commands.Cog):
    """ Music related stuff. """

    def __init__(self, bot):
        self.bot = bot
        self.voice_status = {}

    def get_voice_state(self, guild):
        state = self.voice_status.get(guild.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_status[guild.id] = state
        return state


def setup(bot):
    bot.add_cog(Music(bot))
