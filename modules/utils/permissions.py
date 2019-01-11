from discord.ext import commands
import discord.utils
from modules.utils.configuration import Configuration


def master_check(obj):
    _id = obj.message.author.id
    return _id == obj.bot.configuration.master


def is_master():
    return commands.check(master_check)


def check_perms(obj, perms):
    if master_check(obj):
        return True
    elif not perms:
        return False

    channel = obj.message.channel
    author = obj.message.author
    resolved = channel.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_perms(obj, check, **perms):
    if check_perms(obj, perms):
        return True

    channel = obj.message.channel
    author = obj.message.author
    if channel.is_private:
        return False

    role = discord.utils.find(check, author.roles)
    return role is not None


def mod_or_perms(**perms):
    def kat(obj):
        guild = obj.message.server