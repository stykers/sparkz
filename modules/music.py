import discord
import asyncio
import subprocess
import re
import shlex
import os
import time
import psutil

from discord.ext import commands


class Music(commands.Cog):
    """ Music related features. """

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Music(bot))
