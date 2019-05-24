import discord
import os
import collections
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, context, command = None):
        """The help command."""
        await context.send(embed="Still working on this, sorry.")


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
