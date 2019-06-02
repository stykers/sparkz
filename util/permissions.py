import discord

from util import repository
from discord.ext import commands


async def check_permissions(context, perms, *, check=all):
    if context.author.id in repository.masters:
        return True

    resolved = context.channel.permissions_for(context.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def potato(context):
        return await check_permissions(context, perms, check=check)
    return commands.check(potato)


def can_send(context):
    return isinstance(context.channel, discord.DMChannel) or context.channel.permissions_for(context.guild.me).send_messages


def can_embed(context):
    return isinstance(context.channel, discord.DMChannel) or context.channel.permissions_for(context.guild.me).embed_links


def can_upload(context):
    return isinstance(context.channel, discord.DMChannel) or context.channel.permissions_for(context.guild.me).attach_files


def can_react(context):
    return isinstance(context.channel, discord.DMChannel) or context.channel.permissions_for(context.guild.me).add_reactions


def can_create_invite(context):
    return isinstance(context.channel, discord.DMChannel) or context.channel.permissions_for(context.guild.me).create_invite


def is_nsfw(context):
    return isinstance(context.channel, discord.DMChannel) or context.channel.is_nsfw()
