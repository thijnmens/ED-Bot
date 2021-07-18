from datetime import timedelta
from math import ceil
from discord import Embed, Colour
from discord.ext import commands
from Components.Logging import *

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        Logging.info(f'on_command_error triggered')
        if isinstance(error, commands.BadArgument):
            Logging.info('BadArgument handler ran\n----------')
            await ctx.send('Bad Argument Given')

        elif isinstance(error, commands.CommandNotFound):
            Logging.info('CommandNotFound handler ran\n----------')
            await ctx.send('I don\'t know that command', delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            Logging.info(f'BotMissingPermissions handler ran - {error.missing_perms[0]}\n----------')
            await ctx.send(f'I\'m missing the following permissions: {error.missing_perms[0]}')

        elif isinstance(error, commands.NotOwner):
            Logging.info('NotOwner handler ran\n----------')
            await ctx.send('Owner? You? Don''t make me laugh')

        elif isinstance(error, commands.CommandOnCooldown):
            Logging.info('CommandOnCooldown handler ran\n----------')
            date = str(timedelta(seconds=ceil(error.retry_after))).split(':')
            await ctx.send(f'This command is still on cooldown for: {date[0]} hours, {date[1]} minutes and {date[2]} seconds')

        elif isinstance(error, commands.MissingRequiredArgument):
            Logging.info('MissingRequiredArgument handler ran\n----------')
            await ctx.send(f'Missing Argument(s)')

        elif isinstance(error, commands.MissingPermissions):
            Logging.info('MissingPermissions handler ran\n----------')
            await ctx.send('This command is only for the cool kids, come back when you have the required permission')

        elif isinstance(error, commands.NSFWChannelRequired):
            Logging.info('NSFWChannelRequired hander ran\n----------')
            await ctx.reply('Pervert spotted, initializing the anti-pervert defense systems``')
        
        elif isinstance(error, commands):
            Logging.error(error)
            await ctx.send(embed=Embed(
                title='Uh oh. Something bad happened <a:zerotwomad:866037939258785843>',
                description=f'An unhandled error occured.\nIf this keeps occuring open an [issue report](https://github.com/thijnmens/RogueBot/issues) or go pester that guy who \'coded\' this mess.\n\n```{error}```',
                colour=Colour.red()
            ))

        await self.bot.get_channel(866039275753177158).send(embed=Embed(
        title=f'{ctx.command} in {ctx.guild.name}',
        description=f'{ctx.guild.id}\n**Message Content**```{ctx.message.content}```\n**Error**```{error}```',
        colour=Colour.red()
    ))

def setup(bot):
    bot.add_cog(ErrorHandler(bot))