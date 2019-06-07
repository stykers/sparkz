import discord
import re
import time
import threading

from discord.ext import commands
from util import permissions, essential


class MemberID(commands.Converter):
    async def convert(self, context, argument):
        try:
            m = await commands.MemberConverter().convert(context, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is invalid.") from None
        else:
            return m.id


class ActionReason(commands.Converter):
    async def convert(self, context, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'Exceeded max input length ({len(argument)}/{reason_max})')
        return ret


class Moderate(commands.Cog):
    """Utilities for moderators."""
    bot = None

    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        Moderate.bot = bot

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason: str = None):
        """ Kicks a user from the guild/server. """
        try:
            await member.kick(reason=essential.responsible(context.author, reason))
            await context.send(essential.actionmessage("kick"))
        except Exception as exception:
            await context.send(exception)

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @permissions.has_permissions(manage_nicknames=True)
    async def nickname(self, context, member: discord.Member, *, name: str = None):
        """ Sets nicknames for server members. """
        try:
            await member.edit(nick=name, reason=essential.responsible(context.author, "Configured by moderator."))
            message = f"**{member.name}** is now nicked as **{name}**."
            if name is None:
                message = f"**{member.name}**'s nick has been reset."
            await context.send(message)
        except Exception as e:
            await context.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def ban(self, context, member: MemberID, *, reason: str = None):
        """ Bans users from the current server/guild. """
        try:
            await context.guild.ban(discord.Object(id=member), reason=essential.responsible(context.author, reason))
            await context.send(essential.actionmessage("ban"))
        except Exception as e:
            await context.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def unban(self, context, member: MemberID, *, reason: str = None):
        """ Pardons users from current guild/server. """
        try:
            await context.guild.unban(discord.Object(id=member), reason=essential.responsible(context.author, reason))
            await context.send(essential.actionmessage("unban"))
        except Exception as e:
            await context.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_roles=True)
    async def mute(self, context, member: discord.Member, *, reason: str = None):
        """ Mutes users from current guild/server. """
        message = []
        for role in context.guild.roles:
            if role.name == "Muted":
                message.append(role.id)
        try:
            therole = discord.Object(id=message[0])
        except IndexError as e:
            await context.send(e)
            return await context.send("Please create a role named **Muted**, case-sensitive.")

        try:
            await member.add_roles(therole, reason=essential.responsible(context.author, reason))
            await context.send(essential.actionmessage("mute"))
        except Exception as e:
            await context.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_roles=True)
    async def unmute(self, context, member: discord.Member, *, reason: str = None):
        """ Unmutes users from current guild/server. """
        message = []
        for role in context.guild.roles:
            if role.name == "Muted":
                message.append(role.id)
        try:
            therole = discord.Object(id=message[0])
        except IndexError:
            return await context.send("Please create a role named **Muted**, case-sensitive.")

        try:
            await member.remove_roles(therole, reason=essential.responsible(context.author, reason))
            await context.send(essential.actionmessage("unmute"))
        except Exception as e:
            await context.send(e)

    @commands.group()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def search(self, context):
        """ Search for a user that matches the search term. """
        if context.invoked_subcommand is None:
            _help = await context.bot.formatter.format_help_for(context, context.command)

            for page in _help:
                await context.send(page)

    @search.command(name="playing")
    async def search_playing(self, context, *, search: str):
        loop = [f"{i} | {i.activity.name} ({i.id})" for i in context.guild.members if i.activity if
                (search.lower() in i.activity.name.lower()) and (not i.bot)]
        await essential.formatoutput(
            context, "playing", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @search.command(name="username", aliases=["name"])
    async def search_name(self, context, *, search: str):
        loop = [f"{i} ({i.id})" for i in context.guild.members if search.lower() in i.name.lower() and not i.bot]
        await essential.formatoutput(
            context, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @search.command(name="nickname", aliases=["nick"])
    async def search_nickname(self, context, *, search: str):
        loop = [f"{i.nick} | {i} ({i.id})" for i in context.guild.members if i.nick if
                (search.lower() in i.nick.lower()) and not i.bot]
        await essential.formatoutput(
            context, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @search.command(name="discriminator", aliases=["discrim"])
    async def search_discriminator(self, context, *, search: str):
        if not len(search) is 4 or not re.compile("^[0-9]*$").search(search):
            return await context.send("You must provide exactly 4 digits")

        loop = [f"{i} ({i.id})" for i in context.guild.members if search == i.discriminator]
        await essential.formatoutput(
            context, "discriminator", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @commands.group()
    @commands.guild_only()
    @permissions.has_permissions(manage_messages=True)
    async def prune(self, context):
        """ Removes messages from the current server. """

        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'remove')

    @staticmethod
    async def do_removal(context, limit, predicate, *, before=None, after=None, message=True):
        if limit > 2000:
            return await context.send(f'Too many messages to search given ({limit}/2000)')

        if before is None:
            before = context.message
        else:
            before = discord.Object(id=before)

        if after is not None:
            after = discord.Object(id=after)

        try:
            deleted = await context.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.Forbidden:
            return await context.send('I lack the permission to delete messages.')
        except discord.HTTPException as e:
            return await context.send(f'Error: {e} (try a smaller search?)')

        deleted = len(deleted)
        if message is True:
            deleted = await context.send(f'🚮 Successfully removed {deleted} message{"" if deleted == 1 else "s"}.')
            await Moderate.bot.http.delete_message(deleted.channel.id, deleted.id)
            await Moderate.bot.http.delete_message(context.message.channel.id, context.message.id)

    @prune.command()
    async def embeds(self, context, search=100):
        """Removes messages that have embeds in them."""
        await self.do_removal(context, search, lambda e: len(e.embeds))

    @prune.command()
    async def files(self, context, search=100):
        """Removes messages that have attachments in them."""
        await self.do_removal(context, search, lambda e: len(e.attachments))

    @prune.command()
    async def mentions(self, context, search=100):
        """Removes messages that have mentions in them."""
        await self.do_removal(context, search, lambda e: len(e.mentions) or len(e.role_mentions))

    @prune.command()
    async def images(self, context, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(context, search, lambda e: len(e.embeds) or len(e.attachments))

    @prune.command(name='all')
    async def _remove_all(self, context, search=100):
        """Removes all messages."""
        await self.do_removal(context, search, lambda e: True)

    @prune.command()
    async def user(self, context, member: discord.Member, search=100):
        """Removes all messages by the member."""
        await self.do_removal(context, search, lambda e: e.author == member)

    @prune.command()
    async def contains(self, context, *, substr: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """
        if len(substr) < 3:
            await context.send('The substring length must be at least 3 characters.')
        else:
            await self.do_removal(context, 100, lambda e: substr in e.content)

    @prune.command(name='bots')
    async def _bots(self, context, search=100, prefix=None):
        """Removes a bot user's messages and messages with their optional prefix."""

        getprefix = prefix if prefix else self.config.prefix

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or m.content.startswith(tuple(getprefix))

        await self.do_removal(context, search, predicate)

    @prune.command(name='users')
    async def _users(self, context, prefix=None, search=100):
        """Removes only user messages. """

        def predicate(m):
            return m.author.bot is False

        await self.do_removal(context, search, predicate)

    @prune.command(name='emojis')
    async def _emojis(self, context, search=100):
        """Removes all messages containing custom emoji."""
        custom_emoji = re.compile(r'<(?:a)?:(\w+):(\d+)>')

        def predicate(m):
            return custom_emoji.search(m.content)

        await self.do_removal(context, search, predicate)

    @prune.command(name='reactions')
    async def _reactions(self, context, search=100):
        """Removes all reactions from messages that have them."""

        if search > 2000:
            return await context.send(f'Too many messages to search for ({search}/2000)')

        total_reactions = 0
        async for message in context.history(limit=search, before=context.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await context.send(f'Successfully removed {total_reactions} reactions.')


def setup(bot):
    bot.add_cog(Moderate(bot))
