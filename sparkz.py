import os

from discord.ext.commands import HelpFormatter
from util.data import Bot
from util import permissions, essential
from shutil import copyfile
from discord import LoginFailure

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


print("Checking config files...")
if not os.path.exists(config.json):
    copyfile(config.json.gen, config.json)
    print("Config file generated.\nPlease replace the bot token and master ID with your own data.")
    exit(0)
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
try:
    bot.run(config.token)
except LoginFailure:
    print("Invalid bot token, please make sure you have configured it in config.json")
    exit(1)
except Exception as exception:
    print("Something is preventing me from starting.")
    print(exception)
print("Exiting!")
