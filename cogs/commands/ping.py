from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog, command, slash_command

from discord.ext.commands.context import Context
from discord.commands.context import ApplicationContext


class Ping(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    def _ping(self):
        return f'{self.bot.latency*100:.2f}ms'


    @command(name = 'ping')
    async def ping_message(self, ctx: Context):
        msg = self._ping()
        await ctx.reply(msg, delete_after = 5)


    @slash_command(name = 'ping')
    async def ping_slash(self, inter: ApplicationContext):
        msg = self._ping()
        await inter.response.send_message(msg)


def setup(bot: Bot):
    bot.add_cog(Ping(bot))