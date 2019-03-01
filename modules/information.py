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

        embed = discord.Embed(colour=discord.Color.dark_red())
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(
            name=f"Masters{'' if len(self.config.masters) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in self.config.masters]),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=True)
        embed.add_field(name="RAM", value=f"{ramusage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{repository.version}**", embed=embed)

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, *, user: discord.Member = None):
        """ Retrieve user info. """
        if user is None:
            user = ctx.author

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="User Name", value=user, inline=True)
        embed.add_field(name="Guild Name", value=user.nick if hasattr(user, "nick") else "None", inline=True)
        embed.add_field(name="Register Date", value=essential.date(user.created_at), inline=True)
        embed.add_field(name="Join Date", value=essential.date(user.joined_at), inline=True)

        embed.add_field(
            name="Roles",
            value=', '.join([f"<@&{x.id}>" for x in user.roles if x is not ctx.guild.default_role]) if len(user.roles) > 1 else 'None',
            inline=False
        )

        await ctx.send(content=f"ℹ About **{user.id}**", embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
