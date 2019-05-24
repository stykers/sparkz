import random

import aiohttp
import discord
from discord.ext import commands


class Weeb(commands.Cog):
    """Weeb commands > <"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True)
    async def hug(self, context, member: discord.Member):
        """Hug your senpai/waifu!"""
        author = context.message.author.mention
        mention = member.mention

        hug = "**{0} gave {1} a hug!**"

        choices = ['https://cdn.stykers.moe/img/hug/1.gif', 'https://cdn.stykers.moe/img/hug/2.gif',
                   'https://cdn.stykers.moe/img/hug/3.gif',
                   'https://cdn.stykers.moe/img/hug/4.gif', 'https://cdn.stykers.moe/img/hug/5.gif']

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


def setup(bot):
    bot.add_cog(Weeb(bot))
