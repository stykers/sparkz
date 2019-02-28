import time
import aiohttp
import discord
import asyncio

from asyncio.subprocess import PIPE
from discord.ext import commands
from io import BytesIO
from util import repository, essential, http, writer


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        self._last_result = None

    @commands.command()
    async def staff(self, ctx):
        """ Who am I? """
        if ctx.author.id in self.config.masters:
            return await ctx.send(f"Sparkz at your service, master **{ctx.author.name}**.")
        if ctx.author.id == 468703341816578059:
            return await ctx.send(f"Also, you are my creator!")
        await ctx.send(f"Nope, you ain't part of our staff team.")

    @commands.command()
    @commands.check(repository.is_master)
    async def reload(self, ctx, name: str):
        """ Reloads specified module/plugin """


def setup(bot):
    bot.add_cog(Staff(bot))