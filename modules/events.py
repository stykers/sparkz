import discord
import discord.client
import traceback
import psutil
import os

from datetime import datetime
from discord.user import User
from discord.ext import commands
from discord.ext.commands import errors


from util import essential


async def send_command_help (ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            await send_command_help(ctx)

        elif isinstance(err, errors.CommandInvokeError):
            err = err.original

            _traceback = traceback.format_tb(err.__traceback__)
            _traceback = ''.join(_traceback)
            error = '```py\n{2}{0}: {3}\n```'.format(type(err).__name__, ctx.message.content, _traceback, err)

            await ctx.send(f"An error occurred while the server is interpreting your command.")
            await ctx.send(error)
            # await self.bot.send_message([await self.bot.get_user_info(x) for x in self.config.masters])


def setup(bot):
    bot.add_cog(Events(bot))
