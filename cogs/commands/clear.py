from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog, command, slash_command, has_guild_permissions
from discord import Option

from discord.ext.commands.context import Context
from discord.commands.context import ApplicationContext
from discord.abc import GuildChannel


class Clear(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    async def _clear(self, amount: int, channel: GuildChannel):
        await channel.purge(limit = amount)


    @command(name = 'clear')
    @has_guild_permissions(manage_messages = True)
    async def clear_message(self, ctx: Context, amount: int = 30, channel: GuildChannel = None):
        msg = f'Deleting {amount} messages'
        await ctx.send(msg, delete_after = 5)
        
        channel = channel or ctx.channel
        await self._clear(amount, channel)


    @slash_command(name = 'clear')
    @has_guild_permissions(manage_messages = True)
    async def clear_slash(self, inter: ApplicationContext, amount: int = 30, channel: GuildChannel = None):
        msg = f'Deleting {amount} messages'
        await inter.response.send_message(msg, ephemeral = True)

        channel = channel or inter.channel 
        await self._clear(amount, channel)


def setup(bot: Bot):
    bot.add_cog(Clear(bot))