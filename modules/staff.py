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
        await ctx.send(f"I am restarting <3")
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

    @commands.group()
    @commands.check(repository.is_master)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

            for page in _help:
                await ctx.send(page)

    @config.command(name="play")
    @commands.check(repository.is_master)
    async def play(self, ctx, *, playing: str):
        """ Makes the bot play something. """
        try:
            await self.bot.change_presence(
                activity=discord.Game(type=0, name=playing)
            )
            writer.change_value("config.json", "playing", playing)
            await ctx.send(f"I am now playing **{playing}**.")
        except discord.InvalidArgument as exception:
            await ctx.send(exception)
        except Exception as e:
            await ctx.send(e)

    @config.command(name="dnd")
    @commands.check(repository.is_master)
    async def dnd(self, ctx):
        """ Sets sparkz into DnD mode. """
        try:
            await self.bot.change_presence(
                status=discord.Status.dnd
            )
            await ctx.send(f"I am now in DnD mode.")
        except Exception as exception:
            await ctx.send(exception)

    @config.command(name="idle")
    @commands.check(repository.is_master)
    async def idle(self, ctx):
        """ Sets sparkz into idle mode. """
        try:
            await self.bot.change_presence(
                status=discord.Status.idle
            )
            await ctx.send(f"I am now in idle mode.")
        except Exception as exception:
            await ctx.send(exception)

    @config.command(name="online")
    @commands.check(repository.is_master)
    async def online(self, ctx):
        """ Sets sparkz into online mode. """
        try:
            await self.bot.change_presence(
                status=discord.Status.online
            )
            await ctx.send(f"I am now in online mode.")
        except Exception as exception:
            await ctx.send(exception)

    @config.command(name="username")
    @commands.check(repository.is_master)
    async def username(self, ctx, *, name: str):
        """ Sets new username. """
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f"I am now **{name}**")
        except discord.HTTPException as err:
            await ctx.send(err)

    @config.command(name="nick")
    @commands.check(repository.is_master)
    async def nick(self, ctx, *, name: str = None):
        """ Sets new nick name. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"I am now nicked as **{name}**")
            else:
                await ctx.send("Nickname successfully reset.")
        except Exception as err:
            await ctx.send(err)

    @config.command(name="pfp")
    @commands.check(repository.is_master)
    async def pfp(self, ctx, *, url: str = None):
        """ Sets the pfp of Sparkz. """
        if url is None and len(ctx.message.attachments) == 1:
            url = ctx.message.attachments[0].url
        else:
            url = url.strip('<>') if url else None

        try:
            bio = await http.get(url, res_method="read")
            await self.bot.user.edit(avatar=bio)
            await ctx.send(f"Applied the pfp:\n{url}")
        except aiohttp.InvalidURL:
            await ctx.send("Invalid URL.")
        except discord.InvalidArgument:
            await ctx.send("Invalid file content.")
        except discord.HTTPException as err:
            await ctx.send(err)
        except TypeError as e:
            await ctx.send(e)

    @commands.command()
    @commands.check(repository.is_master)
    async def tell(self, ctx, name: str, *, msg: str):
        """ Sends a specified user a private message. """
        user = await self.bot.get_user_info(name)
        try:
            result = discord.Embed(colour=discord.Colour.blue())
            result.title = "The master has got a message for you."
            result.add_field(name="Master: ", value=ctx.message.author, inline=False)
            result.add_field(name="Message:", value=msg, inline=False)
            result.set_thumbnail(url=ctx.message.author.avatar_url)
            await self.bot.send_message(user, embed=result)
        except:
            await ctx.send(f"Your message failed to deliver.")
        else:
            await ctx.send(f"Message delivered.")


def setup(bot):
    bot.add_cog(Staff(bot))
