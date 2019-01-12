from discord.ext.commands.converter import IDConverter
from discord.ext.commands.errors import BadArgument
import re


def _get_from_servers(bot, getter, argument):
    result = None
    for server in bot.servers:
        result = getattr(server, getter)(argument)
        if result:
            return result
    return result


class GlobalUser(IDConverter):
    """Optimized version of discord.py's converter."""
    def convert(self):
        message = self.ctx.message
        bot = self.ctx.message.bot
        match = self._get_id_match() or re.match(r'<@!([0-9]+)>$', self.argument)
        server = message.server
        result = None
        if match is None:
            if server:
                result = server.get_member_named(self.argument)
            if result is None:
                result = _get_from_servers(bot, 'get_member_named', self.argument)
        else:
            user_id = match.group(1)
            if server:
                result = server.get_member(user_id)
            if result is None:
                result = _get_from_servers(bot, 'get_member', user_id)

        if result is None:
            raise BadArgument('Unknown user!'.format(self.argument))

        return result