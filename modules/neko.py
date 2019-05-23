from discord.ext import commands
import aiohttp
import discord


class Neko(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True, no_pm=True)
    async def neko(self, ctx):
        """Nekos! \\o/ Warning: Some lewd nekos exist :eyes:"""
        async with self.session.get("https://nekos.life/api/neko") as resp:
            nekos = await resp.json()

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_image(url=nekos['neko'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Neko(bot))
