import discord
import re

from discord.ext import commands
from util import permissions, essential


class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is invalid.") from None
        else:
            return m.id


class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'Exceeded max input length ({len(argument)}/{reason_max})')
        return ret


class Moderate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Kicks a user from the guild/server. """
        try:
            await member.kick(reason=essential.responsible(ctx.author, reason))
            await ctx.send(essential.actionmessage("kick"))
        except Exception as exception:
            await ctx.send(exception)

    @commands.command(aliases=["nick"])
    @commands.guild_only()
    @permissions.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        """ Sets nicknames for server members. """
        try:
            await member.edit(nick=name, reason=essential.responsible(ctx.author, "Configured by moderator."))
            message = f"**{member.name}** is now nicked as **{name}**."
            if name is None:
                message = f"**{member.name}**'s nick has been reset."
            await ctx.send(message)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID, *, reason: str = None):
        """ Bans users from the current server/guild. """
        try:
            await ctx.guild.ban(discord.Object(id=member), reason=essential.responsible(ctx.author, reason))
            await ctx.send(essential.actionmessage("ban"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID, *, reason: str = None):
        """ Pardons users from current guild/server. """
        try:
            await ctx.guild.unban(discord.Object(id=member), reason=essential.responsible(ctx.author, reason))
            await ctx.send(essential.actionmessage("unban"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        """ Mutes users from current guild/server. """
        message = []
        for role in ctx.guild.roles:
            if role.name == "Muted":
                message.append(role.id)
        try:
            therole = discord.Object(id=message[0])
        except IndexError as e:
            await ctx.send(e)
            return await ctx.send("Please create a role named **Muted**, case-sensitive.")

        try:
            await member.add_roles(therole, reason=essential.responsible(ctx.author, reason))
            await ctx.send(essential.actionmessage("mute"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """ Unmutes users from current guild/server. """
        message = []
        for role in ctx.guild.roles:
            if role.name == "Muted":
                message.append(role.id)
        try:
            therole = discord.Object(id=message[0])
        except IndexError:
            return await ctx.send("Please create a role named **Muted**, case-sensitive.")

        try:
            await member.remove_roles(therole, reason=essential.responsible(ctx.author, reason))
            await ctx.send(essential.actionmessage("unmute"))
        except Exception as e:
            await ctx.send(e)

    @commands.group()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def search(self, ctx):
        """ Search for a user that matches the search term. """
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @search.command(name="playing")
    async def search_playing(self, ctx, *, search: str):
        loop = [f"{i} | {i.activity.name} ({i.id})" for i in ctx.guild.members if i.activity if (search.lower() in i.activity.name.lower()) and (not i.bot)]
        await essential.formatoutput(
            ctx, "playing", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @search.command(name="username", aliases=["name"])
    async def search_name(self, ctx, *, search: str):
        loop = [f"{i} ({i.id})" for i in ctx.guild.members if search.lower() in i.name.lower() and not i.bot]
        await essential.formatoutput(
            ctx, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @search.command(name="nickname", aliases=["nick"])
    async def search_nickname(self, ctx, *, search: str):
        loop = [f"{i.nick} | {i} ({i.id})" for i in ctx.guild.members if i.nick if (search.lower() in i.nick.lower()) and not i.bot]
        await essential.formatoutput(
            ctx, "name", f"Found **{len(loop)}** on your search for **{search}**", loop
        )

    @search.command(name="discriminator", aliases=["discrim"])
    async def search_discriminator(self, ctx, *, search: str):
        if not len(search) is 4 or not re.compile("^[0-9]*$").search(search):
            return await ctx.send("You must provide exactly 4 digits")

        loop = [f"{i} ({i.id})" for i in ctx.guild.members if search == i.discriminator]
        await essential.formatoutput(
            ctx, "discriminator", f"Found **{len(loop)}** on your search for **{search}**", loop
        )


def setup(bot):
    bot.add_cog(Moderate(bot))
