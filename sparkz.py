import os

from discord.ext.commands import HelpFormatter
from util.data import Bot
from util import permissions, essential

config = essential.get("config.json")
description = """
The Sparkz discord bot
Made by Stykers <3
"""

oauth_url = ""


class HelpFormat(HelpFormatter):
    async def format_help_for(self, context, command_or_bot):
        if permissions.can_react(context):
            await context.message.add_reaction(chr(0x2709))

        return await super().format_help_for(context, command_or_bot)


print("Loading plugins...")
help_attrs = dict(hidden=True)
bot = Bot(
    command_prefix=config.prefix,
    prefix=config.prefix,
    pm_help=True,
    help_attrs=help_attrs,
    formatter=HelpFormat()
)
for file in os.listdir("modules"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"modules.{name}")
for file in os.listdir("plugins"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"plugins.{name}")
print("Contacting discord.")
bot.run(config.token)
print("Exiting!")
