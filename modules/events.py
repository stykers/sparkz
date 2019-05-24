import discord
import discord.client
import traceback
import psutil
import os

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors

from util import essential


async def send_command_help(ctx):
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)


class Events(commands.Cog):
    """Module to handle events."""
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
            if self.config.debug:
                await ctx.send(error)

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown, please try again in {err.retry_after:.2f} seconds.")

        elif isinstance(err, errors.CommandNotFound):
            await ctx.send(f"Command not found.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not self.config.join_message:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if
                              chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)],
                             key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config.join_message)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.author}@{ctx.guild.name} > {ctx.message.clean_content}")
        except AttributeError:
            print(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        print(f'User: {self.bot.user} | Guilds: {len(self.bot.guilds)}')
        await self.bot.change_presence(activity=discord.Game(type=0, name=self.config.playing),
                                       status=discord.Status.online)

    @commands.command()
    async def debug(self, context):
        """ Query if the bot is running in debug mode or not. """
        if self.config.debug is True:
            await context.send("I am running in Debug mode.")
        else:
            await context.send("I am running in Production mode.")


def setup(bot):
    bot.add_cog(Events(bot))
