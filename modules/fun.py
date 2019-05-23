import random
import discord
import json
import secrets
import aiohttp

from io import BytesIO
from discord.ext import commands
from util import list, permissions, http, essential


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True)
    async def hug(self, context, member: discord.Member):
        """Hug your senpai/waifu!"""
        author = context.message.author.mention
        mention = member.mention

        hug = "**{0} gave {1} a hug!**"

        choices = ['https://cdn.stykers.moe/img/hug/1.gif', 'https://cdn.stykers.moe/img/hug/2.gif', 'https://cdn.stykers.moe/img/hug/3.gif',
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

        choices = ['https://cdn.stykers.moe/img/kiss/1.gif', 'https://cdn.stykers.moe/img/kiss/2.gif', 'https://cdn.stykers.moe/img/kiss/3.gif',
                   'https://cdn.stykers.moe/img/kiss/4.gif', 'https://cdn.stykers.moe/img/kiss/5.gif']

        image = random.choice(choices)

        embed = discord.Embed(colour=discord.Colour.blue(), description=kiss.format(author, mention))
        embed.set_image(url=image)

        await context.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def neko(self, ctx):
        """Nekos! \\o/ Warning: Some lewd nekos exist"""
        async with self.session.get("https://nekos.life/api/neko") as resp:
            nekos = await resp.json()

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_image(url=nekos['neko'])
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(list.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you

        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept seed between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await ctx.send(f"I'd rate {thing} a **{num}.{deci} / 100**")

    @commands.command(aliases=['noticemesenpai'])
    async def noticeme(self, ctx):
        """ Notice me senpai! owo """
        if not permissions.can_upload(ctx):
            return await ctx.send("I lack the permission to send images.")

        with open("assets/noticeme.gif", "rb") as fin:
            bio = BytesIO(fin.read())
        await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if a == b == c:
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


def setup(bot):
    bot.add_cog(Fun(bot))
