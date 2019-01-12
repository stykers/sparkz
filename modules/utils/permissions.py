from discord.ext import commands
import discord.utils
from modules.utils.configuration import Configuration


def master_check(ctx):
    _id = ctx.message.author.id
    return _id == ctx.bot.configuration.master


def is_master():
    return commands.check(master_check)


def check_perms(ctx, perms):
    if master_check(ctx):
        return True
    elif not perms:
        return False

    channel = ctx.message.channel
    author = ctx.message.author
    resolved = channel.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_perms(ctx, check, **perms):
    if check_perms(ctx, perms):
        return True

    channel = ctx.message.channel
    author = ctx.message.author
    if channel.is_private:
        return False

    role = discord.utils.find(check, author.roles)
    return role is not None


def mod_or_perms(**perms):
    def kat(ctx):
        mod = ctx.bot.configuration.mod.lower()
        admin = ctx.bot.configuration.admin.lower()
        return role_or_perms(ctx, lambda r: r.name.lower() in (mod, admin), **perms)
    return commands.check(kat)


def admin_or_perms(**perms):
    def kat(ctx):
        admin = ctx.bot.configuration.admin.lower()
        return role_or_perms(ctx, lambda r: r.name.lower() == admin.lower(), **perms)
    return commands.check(kat)


def gowner_or_perms(**perms):
    def kat(ctx):
        if ctx.message.server is None:
            return False
        server = ctx.message.server
        owner = server.owner
        if ctx.message.author.id == owner.id:
            return True
        return check_perms(ctx, perms)
    return commands.check(kat)


def gowner():
    return gowner_or_perms()


def admin():
    return admin_or_perms()


def mod():
    return mod_or_perms()