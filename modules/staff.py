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
    """Utilities for staff members."""
    def __init__(self, bot):
        self.bot = bot
        self.config = essential.get("config.json")
        self._last_result = None

    @commands.command()
    async def staff(self, context):
        """ Who am I? """
        if context.author.id in self.config.masters:
            if context.author.id == 468703341816578059:
                await context.send(f"Sparkz at your service, master **{context.author.name}**.")
                return await context.send(f"You are my creator <3 Thank you for everything!")
            else:
                return await context.send(f"Sparkz at your service, master **{context.author.name}**.")
        await context.send(f"Nooooooooooooooooo :( Please don't hurt me > <")

    @commands.command()
    @commands.check(repository.is_master)
    async def reload(self, context, name: str):
        """ Reloads specified plugin """
        try:
            self.bot.unload_extension(f"plugins.{name}")
            self.bot.load_extension(f"plugins.{name}")
        except Exception as e:
            return await context.send(f"```\n{e}```")
        await context.send(f"**{name}** has been reloaded.")

    @commands.command()
    @commands.check(repository.is_master)
    async def restart(self, context):
        """ Restarts sparkz. """
        await context.send(f"I am restarting <3")
        # time.sleep(1)
        await self.bot.close()

    @commands.command()
    @commands.check(repository.is_master)
    async def shutdown(self, context):
        """ Shuts down sparkz. """
        await context.send(f"I am shutting down =(")
        # time.sleep(1)
        open("shutdown", 'a').close()
        await self.bot.close()

    @commands.command()
    @commands.check(repository.is_master)
    async def load(self, context, name: str):
        """ Loads a plugin that wasn't loaded on startup. """
        try:
            self.bot.load_extension(f"plugins.{name}")
        except Exception as exception:
            return await context.send(f"```diff\n- {exception}```")
        await context.send(f"**{name}** has been loaded.")

    @commands.command()
    @commands.check(repository.is_master)
    async def unload(self, context, name: str):
        """ Unloads a plugin.
        Note that the plugin will still get loaded on startup if it's still on the disk. """
        try:
            self.bot.unload_extension(f"plugins.{name}")
        except Exception as exception:
            return await context.send(f"```diff\n- {exception}```")
        await context.send(f"**{name}** has been unloaded.")

    @commands.command(aliases=['exec', 'execute', 'sh', 'command'])
    @commands.check(repository.is_master)
    async def shell(self, context, *, text: str):
        """ Pass a command to the command interpreter. """
        message = await context.send(f"Please wait...")
        proc = await asyncio.create_subprocess_shell(text, stdin=None, stderr=PIPE, stdout=PIPE)
        out = (await proc.stdout.read()).decode('utf-8').strip()
        err = (await proc.stderr.read()).decode('utf-8').strip()

        if not out and not err:
            await message.delete()
            return await context.message.add_reaction('👌')

        content = ""

        if err:
            content += f"Error:\r\n{err}\r\n{'-' * 30}\r\n"
        if out:
            content += out

        if len(content) > 1500:
            try:
                data = BytesIO(content.encode('utf-8'))
                await message.delete()
                await context.send(content=f"Output exceeded output limit, so a log file is attached.",
                               file=discord.File(data, filename=essential.timetext(f'Output')))
            except asyncio.TimeoutError as e:
                await message.delete()
                return await context.send(e)
        else:
            await message.edit(content=f"```fix\n{content}\n```")

    @commands.group()
    @commands.check(repository.is_master)
    async def config(self, context):
        """Write to the configuration of the bot"""
        if context.invoked_subcommand is None:
            _help = await context.bot.formatter.format_help_for(context, context.command)

            for page in _help:
                await context.send(page)

    @config.command(name="play")
    @commands.check(repository.is_master)
    async def play(self, context, *, playing: str):
        """ Makes the bot play something. """
        try:
            await self.bot.change_presence(
                activity=discord.Game(type=0, name=playing)
            )
            writer.change_value("config.json", "playing", playing)
            await context.send(f"I am now playing **{playing}**.")
        except discord.InvalidArgument as exception:
            await context.send(exception)
        except Exception as e:
            await context.send(e)

    @config.command(name="dnd")
    @commands.check(repository.is_master)
    async def dnd(self, context):
        """ Sets sparkz into DnD mode. """
        try:
            await self.bot.change_presence(
                status=discord.Status.dnd
            )
            await context.send(f"I am now in DnD mode.")
        except Exception as exception:
            await context.send(exception)

    @config.command(name="idle")
    @commands.check(repository.is_master)
    async def idle(self, context):
        """ Sets sparkz into idle mode. """
        try:
            await self.bot.change_presence(
                status=discord.Status.idle
            )
            await context.send(f"I am now in idle mode.")
        except Exception as exception:
            await context.send(exception)

    @config.command(name="online")
    @commands.check(repository.is_master)
    async def online(self, context):
        """ Sets sparkz into online mode. """
        try:
            await self.bot.change_presence(
                status=discord.Status.online
            )
            await context.send(f"I am now in online mode.")
        except Exception as exception:
            await context.send(exception)

    @config.command(name="username")
    @commands.check(repository.is_master)
    async def username(self, context, *, name: str):
        """ Sets new username. """
        try:
            await self.bot.user.edit(username=name)
            await context.send(f"I am now **{name}**")
        except discord.HTTPException as err:
            await context.send(err)

    @config.command(name="nick")
    @commands.check(repository.is_master)
    async def nick(self, context, *, name: str = None):
        """ Sets new nick name. """
        try:
            await context.guild.me.edit(nick=name)
            if name:
                await context.send(f"I am now nicked as **{name}**")
            else:
                await context.send("Nickname successfully reset.")
        except Exception as err:
            await context.send(err)

    @config.command(name="pfp")
    @commands.check(repository.is_master)
    async def pfp(self, context, *, url: str = None):
        """ Sets the pfp of Sparkz. """
        if url is None and len(context.message.attachments) == 1:
            url = context.message.attachments[0].url
        else:
            url = url.strip('<>') if url else None

        try:
            bio = await http.get(url, res_method="read")
            await self.bot.user.edit(avatar=bio)
            await context.send(f"Applied the pfp:\n{url}")
        except aiohttp.InvalidURL:
            await context.send("Invalid URL.")
        except discord.InvalidArgument:
            await context.send("Invalid file content.")
        except discord.HTTPException as err:
            await context.send(err)
        except TypeError as e:
            await context.send(e)

    @commands.command()
    @commands.check(repository.is_master)
    async def tell(self, context, name: str, *, msg: str):
        """ Sends a specified user a private message. """
        user = await self.bot.get_user_info(name)
        try:
            result = discord.Embed(colour=discord.Colour.blue())
            result.title = "The master has got a message for you."
            result.add_field(name="Master: ", value=context.message.author, inline=False)
            result.add_field(name="Message:", value=msg, inline=False)
            result.set_thumbnail(url=context.message.author.avatar_url)
            await user.send('', embed=result)
        except Exception as exception:
            await context.send(f"Your message failed to deliver.")
            # await context.send(exception)
        else:
            await context.send(f"Message delivered.")


def setup(bot):
    bot.add_cog(Staff(bot))
