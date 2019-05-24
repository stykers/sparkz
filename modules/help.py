import discord
import os
import collections
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, context, *module):
        """The help command."""
        if not module:
            content = discord.Embed(title='Overall Help',
                                    description='Use `s!help <module>` to view help of a specific module',
                                    colour=discord.Colour.blue())
            module_description = ''
            for x in self.bot.cogs:
                module_description += ('{} - {}'.format(x, self.bot.cogs[x].__doc__) + '\n')
            content.add_field(name='Modules', value=module_description[0:len(module_description) - 1], inline=False)
            # command_description = ''
            # for y in self.bot.commands:
            #     command_description += ('{} - {}'.format(y.name, y.help) + '\n')
            # content.add_field(name='Commands', value=command_description[0:len(command_description) - 1], inline=False)

            await context.send(embed=content)
        else:
            if len(module) > 1:
                content = discord.Embed(title='Invalid arguments.',
                                        description='Please only request for one module at once.',
                                        colour=discord.Colour.red())
                await context.send(embed=content)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in module:
                        if x == y:
                            content = discord.Embed(title=module[0] + ' Command List', description=self.bot.cogs[module[0]].__doc__)
                            for z in self.bot.get_cog(y).get_commands():
                                if not z.hidden:
                                    content.add_field(name=z.name, value=z.help, inline=False)
                            found = True
                if not found:
                    content = discord.Embed(title='Invalid arguments.', description='The module does not exist.', colour=discord.Colour.red())
                await context.send(embed=content)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
