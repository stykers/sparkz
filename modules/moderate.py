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


def setup(bot):
    bot.add_cog(Moderate(bot))
