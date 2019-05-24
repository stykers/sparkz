import base64
import binascii
import codecs

from discord.ext import commands


class Crypto(commands.Cog):
    """Crypto related utilities."""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def encode(self, context):
        """ All encode methods """
        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'encode')

    @commands.group()
    async def decode(self, context):
        """ All decode methods """
        if context.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await context.invoke(help_cmd, 'decode')

    @staticmethod
    async def encryptout(context, convert, input):
        if len(input) > 1900:
            # TODO: Upload if too long and accept text files
            return await context.send(f"Your result exceeded the maximum output limit, sorry **{context.author.name}**")

        try:
            await context.send(f"📑 **{convert}**```fix\n{input.decode('UTF-8')}```")
        except AttributeError:
            await context.send(f"📑 **{convert}**```fix\n{input}```")

    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, context, *, input: commands.clean_content):
        """ Encode in base32 """
        await self.encryptout(
            context, "Text -> base32", base64.b32encode(input.encode('UTF-8'))
        )

    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, context, *, input: str):
        """ Decode in base32 """
        try:
            await self.encryptout(context, "base32 -> Text", base64.b32decode(input.encode('UTF-8')))
        except Exception:
            await context.send("Invalid base32...")

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, context, *, input: commands.clean_content):
        """ Encode in base64 """
        await self.encryptout(
            context, "Text -> base64", base64.urlsafe_b64encode(input.encode('UTF-8'))
        )

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, context, *, input: str):
        """ Decode in base64 """
        try:
            await self.encryptout(context, "base64 -> Text", base64.urlsafe_b64decode(input.encode('UTF-8')))
        except Exception:
            await context.send("Invalid base64...")

    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, context, *, input: commands.clean_content):
        """ Encode in rot13 """
        await self.encryptout(
            context, "Text -> rot13", codecs.decode(input, 'rot_13')
        )

    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, context, *, input: str):
        """ Decode in rot13 """
        try:
            await self.encryptout(context, "rot13 -> Text", codecs.decode(input, 'rot_13'))
        except Exception:
            await context.send("Invalid rot13...")

    @encode.command(name="hex")
    async def encode_hex(self, context, *, input: commands.clean_content):
        """ Encode in hex """
        await self.encryptout(
            context, "Text -> hex",
            binascii.hexlify(input.encode('UTF-8'))
        )

    @decode.command(name="hex")
    async def decode_hex(self, context, *, input: str):
        """ Decode in hex """
        try:
            await self.encryptout(context, "hex -> Text", binascii.unhexlify(input.encode('UTF-8')))
        except Exception:
            await context.send("Invalid hex...")

    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, context, *, input: commands.clean_content):
        """ Encode in base85 """
        await self.encryptout(
            context, "Text -> base85",
            base64.b85encode(input.encode('UTF-8'))
        )

    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, context, *, input: str):
        """ Decode in base85 """
        try:
            await self.encryptout(context, "base85 -> Text", base64.b85decode(input.encode('UTF-8')))
        except Exception:
            await context.send("Invalid base85...")

    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, context, *, input: commands.clean_content):
        """ Encode in ASCII85 """
        await self.encryptout(
            context, "Text -> ASCII85",
            base64.a85encode(input.encode('UTF-8'))
        )

    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, context, *, input: str):
        """ Decode in ASCII85 """
        try:
            await self.encryptout(context, "ASCII85 -> Text", base64.a85decode(input.encode('UTF-8')))
        except Exception:
            await context.send("Invalid ASCII85...")


def setup(bot):
    bot.add_cog(Crypto(bot))
