import discord

from io import BytesIO
from util import essential
from discord.ext import commands


# noinspection PyBroadException
class DiscordInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")

    @commands.command()
    @commands.guild_only()
    async def pfp(self, ctx, *, user: discord.Member = None):
        """ Get the pfp of you or someone else """
        if user is None:
            user = ctx.author

        await ctx.send(f"Profile picture of **{user.name}**\n{user.avatar_url_as(size=1024)}")

    @pfp.error
    async def pfp_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"That user does not exist!")


def setup(bot):
    bot.add_cog(DiscordInfo(bot))
