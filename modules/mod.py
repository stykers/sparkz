import discord
from discord.ext import commands
from .utils.writer import writer
from .utils import permissions
from datetime import datetime
from collections import deque, defaultdict, OrderedDict
from modules.utils.formatting import escape_mass_mentions, box, pages
import os
import re
import logging
import asyncio

ACTIONS_REPR = {
    'BAN': ('Ban', '\N{HAMMER}'),
    'KICK': ('Kick', '\N{WOMANS BOOTS}'),
    'MUTE': ('Channel Mute', '\N{SPEAKER WITH CENCELLATION STROKE}'),
    'GMUTE': ('Global Mute', '\N{SPEAKER WITH CANCELLATION STROKE}'),
    'SOFTBAN': ('Softban', '\N{DASH SYMBOL} \N{HAMMER}'),
    'FORCEBAN': ('Preemptive ban', '\N{BUST IN SILHOUETTE} \N{HAMMER}'),
    'UNBAN': ('Unban', '\N{DOVE OF PEACE}')
}

ACTION_CASES = {
    'BAN': True,
    'KICK': True,
    'MUTE': False,
    'GMUTE': True,
    'SOFTBAN': True,
    'FORCEBAN': True,
    'UNBAN': True
}

default_config = {
    'ban_tag_spam': False,
    'delete_repeats': True,
    'mod-log': None,
    'respect_hierarchy': False
}

for act, enabled in ACTION_CASES.items():
    act = act.lower() + '_cases'
    default_config[act] = enabled


class ModError(Exception):
    pass


class UnauthorizedCaseEdit(ModError):
    pass


class CaseNotFound(ModError):
    pass


class NoModLogChannel(ModError):
    pass


class TempCache:
    """
    This avoids events involving ban users from triggering twice in logs. It's bad but works.
    """

    def __init__(self, bot):
        self.bot = bot
        self._cache = []

    def add(self, user, server, action, seconds=1):
        tmp = (user.id, server.id, action)
        self._cache.append(tmp)

        async def delete_value():
            await asyncio.sleep(seconds)
            self._cache.remove(tmp)

        self.bot.loop.create_task(delete_value())

    def check(self, user, server, action):
        return (user.id, server.id, action) in self._cache


class Mod:
    """Moderation tools"""

    def __init__(self, bot):
        self.bot = bot
        self.ignore_list = writer.load_json('data/ignorelist.json')
        self.filter = writer.load_json('data/filter.json')
        settings = writer.load_json('data/mod_settings.json')
        self.settings = defaultdict(lambda: default_config.copy(), settings)
        self.cache = OrderedDict()
        self.cases = writer.load_json('data/modlog.json')
        self.last_case = defaultdict(dict, perms_cache)

    @commands.group(pass_context=True, no_pm=True)
    @permissions.gowner_or_perms(administrator=True)
    async def modset(self, ctx):
        """Manages administrator settings."""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await self.bot.send_cmd_help(ctx)
            roles = self.bot.configuration
            msg = ('Admin role: {ADMIN_ROLE}\n'
                   'Mod role: {MOD_ROLE}\n'
                   'Mod-log: {mod-log}\n'
                   'Delete repeats: {delete_repeats}\n'
                   )