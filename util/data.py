from util import permissions
from discord.ext.commands import AutoShardedBot


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, message):
        if not self.is_ready() or message.author.bot or not permissions.can_send(message):
            return

        await self.process_commands(message)