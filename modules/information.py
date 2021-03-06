import time
import discord
import psutil
import os

from discord.ext import commands
from util import repository, essential


class Information(commands.Cog):
    """Module that looks up information."""
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, context):
        """ Ping. """
        before = time.monotonic()
        message = await context.send("Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong   |   {int(ping)}ms")

    @commands.command(aliases=['oauth', 'join'])
    async def invite(self, context):
        """ Generate invite url. """
        await context.send(
            f"**{context.author.name}**, here is the oauth url:\n<{discord.utils.oauth_url(self.bot.user.id)}&permissions=2146958847>"
        )

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, context):
        """ About the bot """
        ramusage = self.process.memory_full_info().rss / 1024 ** 2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embed = discord.Embed(colour=discord.Color.dark_red())
        embed.set_thumbnail(url=context.bot.user.avatar_url)
        embed.add_field(
            name=f"Master{'' if len(self.config.masters) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in self.config.masters]),
            inline=True)
        embed.add_field(name="Homepage", value="https://sparkz.stykers.moe/", inline=True)
        embed.add_field(name="Guilds", value=f"{len(context.bot.guilds)} ( avg: {avgmembers} users/server )", inline=True)
        embed.add_field(name="RAM", value=f"{ramusage:.2f} MiB", inline=True)

        await context.send(content=f"ℹ About **{context.bot.user}** | **{repository.version}**", embed=embed)

    @commands.command()
    @commands.guild_only()
    async def user(self, context, *, user: discord.Member = None):
        """ Retrieve user info. """
        if user is None:
            user = context.author

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="User Name", value=user, inline=True)
        embed.add_field(name="Guild Name", value=user.nick if hasattr(user, "nick") else "None", inline=True)
        embed.add_field(name="Register Date", value=essential.date(user.created_at), inline=True)
        embed.add_field(name="Join Date", value=essential.date(user.joined_at), inline=True)

        embed.add_field(
            name="Roles",
            value=', '.join([f"<@&{x.id}>" for x in user.roles if x is not context.guild.default_role]) if len(
                user.roles) > 1 else 'None',
            inline=False
        )

        await context.send(content=f"ℹ About **{user.id}**", embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pfp(self, context, *, user: discord.Member = None):
        """ Get the pfp of you or someone else """
        if user is None:
            user = context.author
        message = f"Profile picture of **{user.name}**."
        embed = discord.Embed(colour=discord.Colour.blue(), description=message)
        embed.set_image(url=user.avatar_url_as(size=1024))
        await context.send(embed=embed)

    @pfp.error
    async def pfp_handler(self, context, error):
        if isinstance(error, commands.BadArgument):
            await context.send(f"That user does not exist!")


def setup(bot):
    bot.add_cog(Information(bot))
