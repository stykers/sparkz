import time
import aiohttp
import discord
import asyncio

from asyncio.subprocess import PIPE
from discord.ext import commands
from io import BytesIO
from util import repository, essential, http, writer


# noinspection PyBroadException
class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        self._last_result = None

    @commands.command()
    async def staff(self, ctx):
        """ Who am I? """
        if ctx.author.id in self.config.masters:
            return await ctx.send(f"Sparkz at your service, master **{ctx.author.name}**.")
        if ctx.author.id == 468703341816578059:
            return await ctx.send(f"Also, you are my creator!")
        await ctx.send(f"Nope, you ain't part of our staff team.")

    @commands.command()
    @commands.check(repository.is_master)
    async def reload(self, ctx, name: str):
        """ Reloads specified plugin """
        try:
            self.bot.unload_extension(f"plugins.{name}")
            self.bot.load_extension(f"plugins.{name}")
        except Exception as e:
            return await ctx.send(f"```\n{e}```")
        await ctx.send(f"**{name}** has been reloaded.")

    @commands.command()
    @commands.check(repository.is_master)
    async def restart(self, ctx):
        """ Restarts sparkz. """
        await ctx.send(f"I am restarting now :D")
        time.sleep(1)
        await self.bot.logout()

    @commands.command()
    @commands.check(repository.is_master)
    async def load(self, ctx, name: str):
        """ Loads a plugin that wasn't loaded on startup. """
        try:
            self.bot.load_extension(f"plugins.{name}")
        except Exception as exception:
            return await ctx.send(f"```diff\n- {exception}```")
        await ctx.send(f"**{name}** has been loaded.")

    @commands.command()
    @commands.check(repository.is_master)
    async def unload(self, ctx, name: str):
        """ Unloads a plugin. Note that the plugin will still get loaded on startup if it's still on the disk. """
        try:
            self.bot.unload_extension(f"plugins.{name}")
        except Exception as exception:
            return await ctx.send(f"```diff\n- {exception}```")
        await ctx.send(f"**{name}** has been unloaded.")

    @commands.command(aliases=['exec', 'execute', 'sh', 'command'])
    @commands.check(repository.is_master)
    async def shell(self, ctx, *, text: str):
        """ Pass a command to the command interpreter. """
        message = await ctx.send(f"Please wait...")
        proc = await asyncio.create_subprocess_shell(text, stdin=None, stderr=PIPE, stdout=PIPE)
        out = (await proc.stdout.read()).decode('utf-8').strip()
        err = (await proc.stderr.read()).decode('utf-8').strip()

        if not out and not err:
            await message.delete()
            return await ctx.message.add_reaction('👌')

        content = ""

        if err:
            content += f"Error:\r\n{err}\r\n{'-' * 30}\r\n"
        if out:
            content += out

        if len(content) > 1500:
            try:
                data = BytesIO(content.encode('utf-8'))
                await message.delete()
                await ctx.send(content=f"Output exceeded output limit, so a log file is attached.",
                               file=discord.File(data, filename=essential.timetext(f'Output')))
            except asyncio.TimeoutError as e:
                await message.delete()
                return await ctx.send(e)
        else:
            await message.edit(content=f"```fix\n{content}\n```")


def setup(bot):
    bot.add_cog(Staff(bot))