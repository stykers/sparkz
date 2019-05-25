import random
import secrets

from discord.ext import commands
from util import list


class Fun(commands.Cog):
    """Utils and stuff."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball'])
    async def eightball(self, context, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(list.ballresponse)
        await context.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, context):
        """ Coinflip! """
        coinsides = ['Heads', 'Tails']
        await context.send(f"**{context.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def reverse(self, context, *, text: str):
        """esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await context.send(f"🔁 {t_rev}")

    @commands.command()
    async def password(self, context, nbytes: int = 18):
        """ Generates a random password string for you

        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await context.send("I only accept seed between 3-1400")
        if hasattr(context, 'guild') and context.guild is not None:
            await context.send(f"Sending you a private message with your random generated password **{context.author.name}**")
        await context.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rate(self, context, *, thing: commands.clean_content):
        """ Rates what you desire """
        num = random.randint(0, 100)
        deci = random.randint(0, 9)

        if num == 100:
            deci = 0

        await context.send(f"I'd rate {thing} a **{num}.{deci} / 100**")

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, context):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{context.author.name}**,"

        if a == b == c:
            await context.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await context.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await context.send(f"{slotmachine} No match, you lost 😢")


def setup(bot):
    bot.add_cog(Fun(bot))
