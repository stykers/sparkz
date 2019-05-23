from discord.ext import commands
import random
import discord


class Hug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


def setup(bot):
    bot.add_cog(Hug(bot))
