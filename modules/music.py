import discord
import asyncio
import os
import youtube_dl
import glob

from discord.ext import commands
from util import lists
from util import music
from util import essential


useaira = 0
skipsreq = 3
ffbefopts = '-nostdin'
ffopts = '-vn -reconnect 1'
ytdl_npl = youtube_dl.YoutubeDL(lists.ytdl_noplaylist)
ytdl = youtube_dl.YoutubeDL(lists.ytdl_format_options)
ytdl_aria = youtube_dl.YoutubeDL(lists.ytdl_aria)


async def trydel(context, quiet=True):
    try:
        await context.delete()
    except discord.Forbidden:
        if quiet:
            await context.send("I lack the permission to delete messages.")
        else:
            pass
    except AttributeError:
        try:
            await context.message.delete()
        except discord.Forbidden:
            if quiet:
                await context.send("I lack the permission to delete messages.")
            else:
                pass
        except AttributeError:
            print(f"Attribute error! Please report this in an issue.")


class YTDLSource(discord.PCMVolumeTransformer):
    # noinspection PyShadowingNames
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, aria=False):
        loop = loop or asyncio.get_event_loop()
        if aria:
            data = await loop.run_in_executor(None, ytdl_aria.extract_info, url)
        else:
            data = await loop.run_in_executor(None, ytdl_npl.extract_info, url)
        if 'entries' in data:
            data = data['entries'][0]
        filename = (ytdl_npl.prepare_filename(data))
        return cls(discord.FFmpegPCMAudio(filename, before_options=ffbefopts, options=ffopts), data=data)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.requester = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False
        return not self.voice.is_playing()

    @property
    def player(self):
        return self.current.player


class Music(commands.Cog):
    """ Music related stuff. """

    def __init__(self, bot):
        self.bot = bot
        self.voice_status = {}
        self.config = essential.get("config.json")

    def get_voice_state(self, guild):
        state = self.voice_status.get(guild.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_status[guild.id] = state
        return state

    async def create_voice_bot(self, channel):
        voice = await channel.connect()
        state = self.get_voice_state(channel.guild)
        state.voice = voice

    def __unload(self):
        for state in self.voice_status.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    async def playlist(self, context, url):
        state = self.get_voice_state(context.message.guild)
        getinfo = music.exinfo(url, playlist=True)
        for x in getinfo['entries']:
            print(x)
            try:
                await state.songs.put(x['webpage_url'])
            except TypeError:
                pass
            except KeyError:
                await state.songs.put(f"https://www.youtube.com/watch?v={x['url']}")
        if state.voice.is_playing():
            pass
        else:
            await self.getnextsong(context)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        try:
            summoned_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send('You need to be in a voice channel to summon me!')
            await trydel(ctx)
            return False

        state = self.get_voice_state(ctx.message.guild)
        if state.voice is None:
            state.voice = await summoned_channel.connect()
            await ctx.send(f"I have been summoned to `#{summoned_channel}` Channel.")
        else:
            await state.voice.move_to(summoned_channel)
            await ctx.send(f"I have been relocated to `#{summoned_channel}` Channel.")
        return True

    # noinspection PyUnusedLocal
    @commands.command(pass_context=True, no_pm=True)
    async def play(self, context, *, url: str):
        """ Plays a song from a site. """
        state = self.get_voice_state(context.message.guild)
        aria = useaira
        if state.voice is None:
            success = await context.invoke(self.summon)
            if not success:
                return
        if 'playlist?list=' in url:
            await context.send("Passing playlist to daemon... **NOTE: This might take a while!**")
            await self.playlist(context, url)
            return
        try:
            if state.voice.is_playing():
                getinfo = music.exinfo(url, playlist=False)
                print(getinfo)
                if 'entries' in getinfo:
                    FYI = 1
                    getinfo = getinfo['entries'][0]
                    url = getinfo['webpage_url']
                else:
                    FYI = 0
                await context.send(f"Added **{getinfo['title']}**")
                await trydel(context)
                await state.songs.put(url)
                return
        except AttributeError:
            print("Attribute error!")
            pass
        await trydel(context)
        message = await context.send("Processing video...")
        if context.voice_client is not None:
            getinfo = music.exinfo(url, playlist=False)
            print(getinfo)
            if 'entries' in getinfo:
                FYI = 1
                getinfo = getinfo['entries'][0]
                url = getinfo['webpage_url']
            else:
                FYI = 0
            durationsecs = getinfo['duration']
            if durationsecs >= 3600 and self.config.longvids is False:
                return await context.send('This video is over an hour, which is disallowed in the current configuration.')
            if int(aria) == 1:
                state.current = await YTDLSource.from_url(url, loop=self.bot.loop, aria=True)
            else:
                state.current = await YTDLSource.from_url(url, loop=self.bot.loop)
            source = discord.PCMVolumeTransformer(state.current)
            source.volume = volume
            state.current.player = source
            state.requester = str(context.message.author.name)
            await trydel(message)
            m, s = divmod(getinfo['duration'], 60)
            title, vc, avrate = getinfo['title'], getinfo['view_count'], round(getinfo['average_rating'])
            link = getinfo['webpage_url']
            uploader = getinfo['uploader']
            embed = discord.Embed(title='Now Playing', color=0x43B581)
            desclist = [f"Title: {str(title)}\n", f"Length: **{m}m{s}s**\n", f"Views: {str(vc)}\n",
                        f"Average Ratings: {str(avrate)}\n", f"Link: {str(link)}\n", f"Uploaded By: {str(uploader)}\n"]
            if FYI == 1:
                desclist.append("Note: This video is part of a playlist.")
            embed.description = ''.join(desclist)
            embed.set_thumbnail(url=getinfo['thumbnail'])
            await context.send(embed=embed)
            context.voice_client.play(source, after=lambda e: self.nextsongandlog(context))
        else:
            await context.send("I am currently not connected to any channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, context, value=None):
        """ Configure the volume of current song. """
        state = self.get_voice_state(context.message.guild)
        player = state.player
        try:
            value = int(value)
        except ValueError:
            return await context.send("""Unable to set volume!""")
        except TypeError:
            pass
        if value is None:
            await context.send(f'Current Volume: {player.volume:.0%}')
        else:
            global volume
            if state.voice.is_playing():
                player.volume = value / 100
                volume = float(player.volume)
                await context.send(f'Set the volume to {player.volume:.0%}')
            else:
                volume = float(player.volume)
                await context.send(f'Set the volume to {player.volume:.0%} for the next song.')

    async def getnextsong(self, context):
        state = self.get_voice_state(context.message.guild)
        if context.voice_client is None:
            return
        try:
            songurl = state.songs.get_nowait()
        except asyncio.QueueEmpty:
            return
        getinfo = music.exinfo(songurl, playlist=False)
        if getinfo is None:
            return await self.getnextsong(context)
        durationsecs = getinfo['duration']
        if durationsecs >= 3600 and self.config.longvids is False:
            await self.getnextsong(context)
            return await context.send('This video is over an hour, which is disallowed in the current configuration.')
        if useaira == 1:
            state.current = await YTDLSource.from_url(songurl, loop=self.bot.loop, aria=True)
        else:
            state.current = await YTDLSource.from_url(songurl, loop=self.bot.loop)
        source = discord.PCMVolumeTransformer(state.current)
        source.volume = volume
        state.current.player = source
        m, s = divmod(getinfo['duration'], 60)
        title, vc, avrate = getinfo['title'], getinfo['view_count'], round(getinfo['average_rating'])
        link = getinfo['webpage_url']
        uploader = getinfo['uploader']
        embed = discord.Embed(title='Now Playing', color=0x43B581)
        desclist = [f"Title: {title}\n", f"Length: **{m}m{s}s**\n", f"Views: {vc}\n", f"Average Ratings: {avrate}\n",
                    f"Link: {link}\n", f"Uploaded By: {uploader}\n"]
        embed.description = ''.join(desclist)
        embed.set_thumbnail(url=getinfo['thumbnail'])
        await context.send(embed=embed)
        context.voice_client.play(source, after=lambda e: self.nextsongandlog(context))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, context):
        """ Pause/resume the currently playing song. """
        state = self.get_voice_state(context.message.guild)
        if state.voice.is_paused():
            context.send("Paused current music.")
            state.voice.resume()
        else:
            context.send("Resumed current music.")
            state.voice.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def disconnect(self, context):
        """ Stops playing audio and leaves the voice channel. This also clears the queue. """
        guild = context.message.guild
        state = self.get_voice_state(context.message.guild)
        state.current = None
        if state.is_playing():
            player = state.player
            try:
                player.stop()
            except AttributeError:
                pass
        try:
            del self.voice_status[guild.id]
            await state.voice.disconnect()
            await context.send(f"Disconnected From `#{state.voice.channel.name}`.")
        except Exception as e:
            print(e)
            pass
        for file in glob.glob('youtube-*.*'):
            try:
                os.remove(file)
            except PermissionError:
                pass

    def nextsongandlog(self, ctx):
        print("next song")
        coro = self.getnextsong(ctx)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        try:
            result = fut.result()
            print(result)
        except Exception as e:
            print(e)
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, context):
        """ A skip vote, 3 votes will make the song skip. """
        state = self.get_voice_state(context.message.guild)
        if not state.voice.is_playing():
            await context.send('I am not playing any music...')
            return
        voter = context.message.author
        if voter.name == state.requester:
            await context.send('Requester requested to skip song. skipping now...')
            state.skip_votes.clear()
            if state.voice.is_playing():
                state.voice.stop()
                await self.getnextsong(context)
        elif (context.message.channel.permissions_for(context.message.author)).move_members:
            await context.send(f'{context.message.author.name} forced a skip. Skipping...')
            state.skip_votes.clear()
            if state.voice.is_playing():
                state.voice.stop()
                await self.getnextsong(context)
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= skipsreq:
                votemessage = await context.say('Skipping song...')
                await asyncio.sleep(1)
                await trydel(votemessage)
                state.skip_votes.clear()
                if state.voice.is_playing():
                    state.voice.stop()
                    await self.getnextsong(context)
            else:
                await context.send(f'Skip vote added, currently at [{total_votes}/{skipsreq}]')
        else:
            await context.send(f'You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, context):
        """ Shows info about the queue. """
        state = self.get_voice_state(context.message.guild)
        skip_count = len(state.skip_votes)
        queue = []
        dembed = discord.Embed(title="Playlist:", color=0x7289DA)
        try:
            if state.current is None:
                dembed.add_field(name="Currently playing:", value="Nothing.")
                return await context.send(embed=dembed)
            lst = list(state.songs._queue)
            for x in lst[:5]:
                info = music.exinfo(x)
                m, s = divmod(info['duration'], 60)
                y = f"""Title: **{info['title']}**\nLength: **{m}m{s}s**\n"""
                queue.append(y)
            if len(lst) > 5:
                queue.append("{} More Not listed.".format(str(len(lst) - 5)))

            fqueue = ''.join(queue)
            cm, cs = divmod(state.current.data['duration'], 60)
            dembed.add_field(name='Currently playing:',
                             value='Title: **{}**\nLength: **{}m{}s**\n[skips: {}/3]'.format(
                                 state.current.data['title'],
                                 cm, cs, skip_count))
            if not fqueue == '':
                dembed.add_field(name='Up Next:', value=fqueue)
            else:
                pass
            await context.send(embed=dembed)
        except AttributeError:
            print("Attribute error!")


def setup(bot):
    bot.add_cog(Music(bot))
