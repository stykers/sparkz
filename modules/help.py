import discord
import os
import collections
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, context, *module):
        """The help command."""
        if not module:
            content = discord.Embed(title='Overall Help', description='Use `s!help <module>` to view help of a specific module')
            await context.send(embed=content)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
