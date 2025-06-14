from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog, command, slash_command
from discord import Option, Member, Embed

from discord.ext.commands.context import Context
from discord.commands.context import ApplicationContext

    
class Avatar(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    async def _avatar(self, user: Member, _type: str = 'normal'):
        options = {
            'normal': user.avatar,
            'guild': user.guild_avatar,
        }
        
        if not options.get(_type) or not options[_type]: return

        embed = Embed()

        embed.title = user.nick or user.name
        embed.colour = 0
        embed.set_image(url = options[_type])

        return embed


    @command(name = 'avatar')
    async def avatar_message(self, ctx: Context, member: Member = None):
        user = member or ctx.author
        embed = await self._avatar(user)
        await ctx.message.reply(embed = embed)


    @slash_command(name = 'avatar')
    async def avatar_slash(self, inter: ApplicationContext, member: Member = None, type: str = Option(str, choices = ['normal', 'guild'], default = 'normal')):
        user = member or inter.author
        embed = await self._avatar(user, type)

        if not embed: await inter.interaction.respond('Image not found')
        else: await inter.interaction.respond(embed = embed)


def setup(bot: Bot):
    bot.add_cog(Avatar(bot))