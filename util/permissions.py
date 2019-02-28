import discord

from util import repository
from discord.ext import commands


async def check_permissions(ctx, perms, *, check=all):
    if ctx.author.id in repository.masters:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())