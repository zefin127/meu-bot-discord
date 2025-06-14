from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog

from discord import Member, Embed, Colour

class MemberRemove(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
 
    @Cog.listener('on_member_remove')
    async def on_member_remove(self, member: Member):
        guild = await self.bot.fetch_guild(1381743234015035547)
        channel = await guild.fetch_channel(1382820016583479346)

        embed = Embed(
            title = f'{member.name}#{member.discriminator} Saiu do servidor',
            colour = Colour.red()
        ) 

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f'ID: {member.id}')       
        await channel.send(embed=embed)
    

def setup(bot: Bot):
    bot.add_cog(MemberRemove(bot))
    print('MemberRemove cog loaded successfully.') 




    
