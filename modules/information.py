import time
import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from util import repository, essential


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Ping. """
        before = time.monotonic()
        message = await ctx.send("Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong   |   {int(ping)}ms")

    @commands.command(aliases=['oauth', 'join'])
    async def invite(self, ctx):
        """ Generate invite url. """
        await ctx.send(
            f"**{ctx.author.name}**, here is the oauth url:\n<{discord.utils.oauth_url(self.bot.user.id)}>"
        )

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        ramusage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embed = discord.Embed(colour=ctx.me.top_role.colour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(
            name=f"Developer{'' if len(self.config.masters) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in self.config.masters]),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=True)
        embed.add_field(name="RAM", value=f"{ramusage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{repository.version}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
