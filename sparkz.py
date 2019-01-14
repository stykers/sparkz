import os
import sys
import asyncio

sys.path.insert(0, 'lib')
import logging
import logging.handlers
import traceback
import datetime
import subprocess
from discord.ext import commands
import discord
from modules.utils.configuration import Configuration
from modules.utils.writer import writer
from modules.utils.formatting import code_single
from collections import Counter
from io import TextIOWrapper

intro = 'Sparkz - Discord bot'


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # noinspection PyUnusedLocal
        # TODO: add per server prefix
        def prefix(bot, message):
            """Returns the prefix of the bot."""
            return bot.configuration.prefixes()

        self.counter = Counter()
        self.uptime = datetime.datetime.utcnow()
        self._message_modifiers = []
        self.configuration = Configuration()
        self._intro_displayed = False
        self._shutdown_mode = None
        self.logger = set_logger(self)
        self._last_exception = None
        self.oauth_url = ''

        try:
            self._plugin_repo = writer.load_json('data/repo.json')
        except Exception:
            self._plugin_repo = {}

        if 'self_bot' in kwargs:
            self.configuration.self_bot = kwargs['self_bot']
        else:
            kwargs['self_bot'] = self.configuration.self_bot
            if self.configuration.self_bot:
                kwargs['pm_help'] = False
        super().__init__(*args, command_prefix=prefix, **kwargs)

    async def send_message(self, *args, **kwargs):
        if self._message_modifiers:
            if 'content' in kwargs:
                pass
            elif len(args) == 2:
                args = list(args)
                kwargs['content'] = args.pop()
            else:
                return await super().send_message(*args, **kwargs)

            content = kwargs['content']
            for m in self._message_modifiers:
                try:
                    content = str(m(content))
                except:
                    pass
            kwargs['content'] = content
        return await super.send_message(*args, **kwargs)

    async def shutdown(self, restart=False):
        """Exit with return value 0, if the bot is going to restart it will exit with 127 so the launcher will restart
        it."""
        self._shutdown_mode = not restart
        await self.logout()

    def add_message_modifier(self, func):
        """This will process a message passed in to this in to a modified message."""
        if not callable(func):
            raise TypeError('This function must be callable!')

        self._message_modifiers.append(func)

    def remove_message_modifier(self, func):
        """Removes message modifier."""
        if func not in self._message_modifiers:
            raise RuntimeError('Function is not in message modifiers!')

        self._message_modifiers.remove(func)

    def clear_message_modifiers(self):
        """Removes all modifiers."""
        self._message_modifiers.clear()

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = self.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.send_message(ctx.message.channel, page)
        else:
            pages = self.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.send_message(ctx.message.channel, page)

    @staticmethod
    def user_allowed(message):
        author = message.author

        if author.bot:
            return False

        if author == self.user:
            return self.configuration.self_bot

        mod_module = self.get_module('Mod')
        global_ignores = self.get_module('Master')