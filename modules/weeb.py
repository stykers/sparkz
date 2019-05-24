import random

import aiohttp
import discord
from discord.ext import commands
from util import permissions
from io import BytesIO


class Weeb(commands.Cog):
    """Weeb commands > <"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(aliases=['noticemesenpai'])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def noticeme(self, context):
        """ Notice me senpai! owo """
        if not permissions.can_upload(context):
            return await context.send("I lack the permission to send images.")

        with open("assets/noticeme.gif", "rb") as fin:
            bio = BytesIO(fin.read())
        await context.send(file=discord.File(bio, filename="noticeme.gif"))

    @commands.command(pass_context=True)
    async def hug(self, context, member: discord.Member):
        """Hug your senpai/waifu!"""
        author = context.message.author.mention
        mention = member.mention

        hug = "**{0} gave {1} a hug!**"

        choices = ['https://cdn.stykers.moe/img/hug/1.gif', 'https://cdn.stykers.moe/img/hug/2.gif',
                   'https://cdn.stykers.moe/img/hug/3.gif', 'https://cdn.stykers.moe/img/hug/4.gif',
                   'https://cdn.stykers.moe/img/hug/5.gif', 'https://cdn.stykers.moe/img/hug/6.gif',
                   'https://cdn.stykers.moe/img/hug/7.gif', 'https://cdn.stykers.moe/img/hug/8.gif',
                   'https://cdn.stykers.moe/img/hug/9.gif', 'https://cdn.stykers.moe/img/hug/10.gif',
                   'https://cdn.stykers.moe/img/hug/11.gif', 'https://cdn.stykers.moe/img/hug/12.gif',
                   'https://cdn.stykers.moe/img/hug/13.gif', 'https://cdn.stykers.moe/img/hug/14.gif',
                   'https://cdn.stykers.moe/img/hug/15.gif', 'https://cdn.stykers.moe/img/hug/16.gif',
                   'https://cdn.stykers.moe/img/hug/17.gif', 'https://cdn.stykers.moe/img/hug/18.gif',
                   'https://cdn.stykers.moe/img/hug/19.gif', 'https://cdn.stykers.moe/img/hug/20.gif',
                   'https://cdn.stykers.moe/img/hug/21.gif', 'https://cdn.stykers.moe/img/hug/22.gif',
                   'https://cdn.stykers.moe/img/hug/23.gif', 'https://cdn.stykers.moe/img/hug/24.gif',
                   'https://cdn.stykers.moe/img/hug/25.gif', 'https://cdn.stykers.moe/img/hug/26.gif',
                   'https://cdn.stykers.moe/img/hug/27.gif', 'https://cdn.stykers.moe/img/hug/28.gif',
                   'https://cdn.stykers.moe/img/hug/29.gif']

        image = random.choice(choices)

        embed = discord.Embed(colour=discord.Colour.blue(), description=hug.format(author, mention))
        embed.set_image(url=image)

        await context.send(embed=embed)

    @commands.command(pass_context=True)
    async def kiss(self, context, member: discord.Member):
        """Kiss your senpai/waifu!"""
        author = context.message.author.mention
        mention = member.mention

        kiss = "**{0} gave {1} a kiss!**"

        choices = ['https://cdn.stykers.moe/img/kiss/1.gif', 'https://cdn.stykers.moe/img/kiss/2.gif',
                   'https://cdn.stykers.moe/img/kiss/3.gif',
                   'https://cdn.stykers.moe/img/kiss/4.gif', 'https://cdn.stykers.moe/img/kiss/5.gif']

        image = random.choice(choices)

        embed = discord.Embed(colour=discord.Colour.blue(), description=kiss.format(author, mention))
        embed.set_image(url=image)

        await context.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def neko(self, context):
        """Nekos! \\o/ Warning: Some lewd nekos exist o_o"""
        async with self.session.get("https://nekos.life/api/neko") as resp:
            nekos = await resp.json()

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_image(url=nekos['neko'])
        await context.send(embed=embed)

    @commands.command(pass_context=True)
    async def poke(self, context, member: discord.Member):
        """Poke someone!"""
        author = context.message.author.mention
        mention = member.mention

        poke = "**{0} poked {1}!**"

        choices = ['https://cdn.stykers.moe/img/poke/1.gif', 'https://cdn.stykers.moe/img/poke/2.gif',
                   'https://cdn.stykers.moe/img/poke/3.gif', 'https://cdn.stykers.moe/img/poke/4.gif',
                   'https://cdn.stykers.moe/img/poke/5.gif', 'https://cdn.stykers.moe/img/poke/6.gif',
                   'https://cdn.stykers.moe/img/poke/7.gif', 'https://cdn.stykers.moe/img/poke/8.gif',
                   'https://cdn.stykers.moe/img/poke/9.gif', 'https://cdn.stykers.moe/img/poke/10.gif',
                   'https://cdn.stykers.moe/img/poke/11.gif', 'https://cdn.stykers.moe/img/poke/12.gif',
                   'https://cdn.stykers.moe/img/poke/13.gif', 'https://cdn.stykers.moe/img/poke/14.gif',
                   'https://cdn.stykers.moe/img/poke/15.gif', 'https://cdn.stykers.moe/img/poke/16.gif',
                   'https://cdn.stykers.moe/img/poke/17.gif']

        image = random.choice(choices)

        embed = discord.Embed(description=poke.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await context.send(embed=embed)

    @commands.command(pass_context=True)
    async def slap(self, context, member: discord.Member):
        """Slap a meanie!"""
        author = context.message.author.mention
        mention = member.mention

        slap = "**{0} slapped {1}!**"

        choices = ['https://cdn.stykers.moe/img/slap/1.gif', 'https://cdn.stykers.moe/img/slap/2.gif',
                   'https://cdn.stykers.moe/img/slap/3.gif', 'https://cdn.stykers.moe/img/slap/4.gif',
                   'https://cdn.stykers.moe/img/slap/5.gif', 'https://cdn.stykers.moe/img/slap/6.gif',
                   'https://cdn.stykers.moe/img/slap/7.gif', 'https://cdn.stykers.moe/img/slap/8.gif',
                   'https://cdn.stykers.moe/img/slap/9.gif', 'https://cdn.stykers.moe/img/slap/10.gif',
                   'https://cdn.stykers.moe/img/slap/11.gif', 'https://cdn.stykers.moe/img/slap/12.gif',
                   'https://cdn.stykers.moe/img/slap/13.gif', 'https://cdn.stykers.moe/img/slap/14.gif',
                   'https://cdn.stykers.moe/img/slap/15.gif', 'https://cdn.stykers.moe/img/slap/16.gif',
                   'https://cdn.stykers.moe/img/slap/17.gif', 'https://cdn.stykers.moe/img/slap/18.gif',
                   'https://cdn.stykers.moe/img/slap/19.gif', 'https://cdn.stykers.moe/img/slap/20.gif',
                   'https://cdn.stykers.moe/img/slap/21.gif', 'https://cdn.stykers.moe/img/slap/22.gif',
                   'https://cdn.stykers.moe/img/slap/23.gif', 'https://cdn.stykers.moe/img/slap/24.gif',
                   'https://cdn.stykers.moe/img/slap/25.gif', 'https://cdn.stykers.moe/img/slap/26.gif',
                   'https://cdn.stykers.moe/img/slap/27.gif']

        image = random.choice(choices)

        embed = discord.Embed(description=slap.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await context.send(embed=embed)

    @commands.command(pass_context=True)
    async def fistbump(self, context, member: discord.Member):
        """Give someone a fistbump =)"""
        author = context.message.author.mention
        mention = member.mention

        hug = "**{0} gave {1} a fistbump!**"

        choices = ['https://cdn.stykers.moe/img/fistbump/1.gif', 'https://cdn.stykers.moe/img/fistbump/2.gif',
                   'https://cdn.stykers.moe/img/fistbump/3.gif', 'https://cdn.stykers.moe/img/fistbump/4.gif',
                   'https://cdn.stykers.moe/img/fistbump/5.gif', 'https://cdn.stykers.moe/img/fistbump/6.gif',
                   'https://cdn.stykers.moe/img/fistbump/7.gif', 'https://cdn.stykers.moe/img/fistbump/8.gif',
                   'https://cdn.stykers.moe/img/fistbump/9.gif', 'https://cdn.stykers.moe/img/fistbump/10.gif',
                   'https://cdn.stykers.moe/img/fistbump/11.gif', 'https://cdn.stykers.moe/img/fistbump/12.gif',
                   'https://cdn.stykers.moe/img/fistbump/13.gif', 'https://cdn.stykers.moe/img/fistbump/14.gif',
                   'https://cdn.stykers.moe/img/fistbump/15.gif', 'https://cdn.stykers.moe/img/fistbump/16.gif',
                   'https://cdn.stykers.moe/img/fistbump/17.gif', 'https://cdn.stykers.moe/img/fistbump/18.gif',
                   'https://cdn.stykers.moe/img/fistbump/19.gif', 'https://cdn.stykers.moe/img/fistbump/20.gif',
                   'https://cdn.stykers.moe/img/fistbump/21.gif', 'https://cdn.stykers.moe/img/fistbump/22.gif',
                   'https://cdn.stykers.moe/img/fistbump/23.gif']

        image = random.choice(choices)

        embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour(0xba4b5b))
        embed.set_image(url=image)

        await context.send(embed=embed)

    @commands.command(pass_context=True)
    async def smug(self, context):
        """Smug on everyone xD"""
        author = context.message.author.mention

        smug = "**{0} your smug image.**"

        choices = ['https://cdn.stykers.moe/img/smug/129.jpg', 'https://cdn.stykers.moe/img/smug/120.jpg',
                   'https://cdn.stykers.moe/img/smug/123.jpg', 'https://cdn.stykers.moe/img/smug/27.png',
                   'https://cdn.stykers.moe/img/smug/55.png', 'https://cdn.stykers.moe/img/smug/93.png',
                   'https://cdn.stykers.moe/img/smug/24.jpg', 'https://cdn.stykers.moe/img/smug/15.jpg',
                   'https://cdn.stykers.moe/img/smug/83.png', 'https://cdn.stykers.moe/img/smug/130.jpg',
                   'https://cdn.stykers.moe/img/smug/109.jpg', 'https://cdn.stykers.moe/img/smug/114.png',
                   'https://cdn.stykers.moe/img/smug/100.jpg', 'https://cdn.stykers.moe/img/smug/38.png',
                   'https://cdn.stykers.moe/img/smug/71.png', 'https://cdn.stykers.moe/img/smug/7.jpg',
                   'https://cdn.stykers.moe/img/smug/16.jpg', 'https://cdn.stykers.moe/img/smug/116.jpg',
                   'https://cdn.stykers.moe/img/smug/19.jpg', 'https://cdn.stykers.moe/img/smug/82.jpg',
                   'https://cdn.stykers.moe/img/smug/117.jpg', 'https://cdn.stykers.moe/img/smug/127.jpg',
                   'https://cdn.stykers.moe/img/smug/35.jpg', 'https://cdn.stykers.moe/img/smug/87.png',
                   'https://cdn.stykers.moe/img/smug/80.png', 'https://cdn.stykers.moe/img/smug/53.jpg',
                   'https://cdn.stykers.moe/img/smug/132.png', 'https://cdn.stykers.moe/img/smug/4.png',
                   'https://cdn.stykers.moe/img/smug/23.jpg', 'https://cdn.stykers.moe/img/smug/14.jpg',
                   'https://cdn.stykers.moe/img/smug/81.jpg', 'https://cdn.stykers.moe/img/smug/22.jpg',
                   'https://cdn.stykers.moe/img/smug/119.jpg', 'https://cdn.stykers.moe/img/smug/124.png',
                   'https://cdn.stykers.moe/img/smug/103.jpg', 'https://cdn.stykers.moe/img/smug/135.png',
                   'https://cdn.stykers.moe/img/smug/13.png', 'https://cdn.stykers.moe/img/smug/107.jpg',
                   'https://cdn.stykers.moe/img/smug/101.jpg', 'https://cdn.stykers.moe/img/smug/20.jpg',
                   'https://cdn.stykers.moe/img/smug/40.png', 'https://cdn.stykers.moe/img/smug/131.jpg',
                   'https://cdn.stykers.moe/img/smug/6.jpg', 'https://cdn.stykers.moe/img/smug/37.jpg',
                   'https://cdn.stykers.moe/img/smug/50.jpg', 'https://cdn.stykers.moe/img/smug/111.jpg',
                   'https://cdn.stykers.moe/img/smug/68.jpg', 'https://cdn.stykers.moe/img/smug/34.jpg',
                   'https://cdn.stykers.moe/img/smug/63.jpg', 'https://cdn.stykers.moe/img/smug/110.jpg',
                   'https://cdn.stykers.moe/img/smug/48.png', 'https://cdn.stykers.moe/img/smug/64.jpg',
                   'https://cdn.stykers.moe/img/smug/28.jpg', 'https://cdn.stykers.moe/img/smug/41.png',
                   'https://cdn.stykers.moe/img/smug/122.png', 'https://cdn.stykers.moe/img/smug/18.jpg',
                   'https://cdn.stykers.moe/img/smug/102.png', 'https://cdn.stykers.moe/img/smug/91.jpg',
                   'https://cdn.stykers.moe/img/smug/49.jpg', 'https://cdn.stykers.moe/img/smug/43.png',
                   'https://cdn.stykers.moe/img/smug/89.jpg', 'https://cdn.stykers.moe/img/smug/75.png',
                   'https://cdn.stykers.moe/img/smug/108.jpg', 'https://cdn.stykers.moe/img/smug/8.jpg',
                   'https://cdn.stykers.moe/img/smug/51.jpg', 'https://cdn.stykers.moe/img/smug/99.png',
                   'https://cdn.stykers.moe/img/smug/57.jpg', 'https://cdn.stykers.moe/img/smug/61.jpg',
                   'https://cdn.stykers.moe/img/smug/94.jpg', 'https://cdn.stykers.moe/img/smug/26.png',
                   'https://cdn.stykers.moe/img/smug/118.png', 'https://cdn.stykers.moe/img/smug/2.jpg',
                   'https://cdn.stykers.moe/img/smug/30.jpg', 'https://cdn.stykers.moe/img/smug/90.jpg',
                   'https://cdn.stykers.moe/img/smug/113.png', 'https://cdn.stykers.moe/img/smug/3.jpg',
                   'https://cdn.stykers.moe/img/smug/47.png', 'https://cdn.stykers.moe/img/smug/60.jpg',
                   'https://cdn.stykers.moe/img/smug/112.png', 'https://cdn.stykers.moe/img/smug/12.png',
                   'https://cdn.stykers.moe/img/smug/59.png', 'https://cdn.stykers.moe/img/smug/17.png',
                   'https://cdn.stykers.moe/img/smug/84.jpg', 'https://cdn.stykers.moe/img/smug/126.png',
                   'https://cdn.stykers.moe/img/smug/134.png', 'https://cdn.stykers.moe/img/smug/79.jpg',
                   'https://cdn.stykers.moe/img/smug/72.png', 'https://cdn.stykers.moe/img/smug/92.png',
                   'https://cdn.stykers.moe/img/smug/32.jpg', 'https://cdn.stykers.moe/img/smug/56.jpg',
                   'https://cdn.stykers.moe/img/smug/121.jpg', 'https://cdn.stykers.moe/img/smug/105.jpg',
                   'https://cdn.stykers.moe/img/smug/39.jpg', 'https://cdn.stykers.moe/img/smug/21.png',
                   'https://cdn.stykers.moe/img/smug/29.jpg', 'https://cdn.stykers.moe/img/smug/66.png',
                   'https://cdn.stykers.moe/img/smug/65.jpg', 'https://cdn.stykers.moe/img/smug/133.jpg',
                   'https://cdn.stykers.moe/img/smug/9.jpg', 'https://cdn.stykers.moe/img/smug/106.jpg',
                   'https://cdn.stykers.moe/img/smug/36.jpg', 'https://cdn.stykers.moe/img/smug/70.jpg',
                   'https://cdn.stykers.moe/img/smug/128.png', 'https://cdn.stykers.moe/img/smug/96.png',
                   'https://cdn.stykers.moe/img/smug/42.jpg', 'https://cdn.stykers.moe/img/smug/54.png',
                   'https://cdn.stykers.moe/img/smug/77.jpg', 'https://cdn.stykers.moe/img/smug/97.jpg',
                   'https://cdn.stykers.moe/img/smug/10.png', 'https://cdn.stykers.moe/img/smug/46.jpg',
                   'https://cdn.stykers.moe/img/smug/78.jpg', 'https://cdn.stykers.moe/img/smug/125.jpg',
                   'https://cdn.stykers.moe/img/smug/73.jpg', 'https://cdn.stykers.moe/img/smug/76.jpg',
                   'https://cdn.stykers.moe/img/smug/52.png', 'https://cdn.stykers.moe/img/smug/44.jpg',
                   'https://cdn.stykers.moe/img/smug/67.png', 'https://cdn.stykers.moe/img/smug/25.png',
                   'https://cdn.stykers.moe/img/smug/104.jpg', 'https://cdn.stykers.moe/img/smug/86.jpg',
                   'https://cdn.stykers.moe/img/smug/11.jpg', 'https://cdn.stykers.moe/img/smug/5.jpg',
                   'https://cdn.stykers.moe/img/smug/58.jpg', 'https://cdn.stykers.moe/img/smug/95.jpg',
                   'https://cdn.stykers.moe/img/smug/88.jpg', 'https://cdn.stykers.moe/img/smug/98.png',
                   'https://cdn.stykers.moe/img/smug/115.jpg', 'https://cdn.stykers.moe/img/smug/62.jpg',
                   'https://cdn.stykers.moe/img/smug/31.jpg', 'https://cdn.stykers.moe/img/smug/1.jpg',
                   'https://cdn.stykers.moe/img/smug/45.jpg', 'https://cdn.stykers.moe/img/smug/85.jpg',
                   'https://cdn.stykers.moe/img/smug/74.png']

        image = random.choice(choices)

        embed = discord.Embed(description=smug.format(author), colour=discord.Colour(0x644aba))
        embed.set_image(url=image)

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Weeb(bot))
