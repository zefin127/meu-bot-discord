from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog

from discord import Message, Embed, Color

class MessageDelete(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @Cog.listener('on_message_delete')
    async def message_delete(self, message: Message):
        if message.author.bot: return
        
        print(f'👤 Autor da mensagem: {message.author}')
        print(f'📢 Canal onde a mensagem foi apagada: #{message.channel.name}')
        print(f'📄 Conteúdo da mensagem excluída: {message.content}')
        
        log_channel_id = 1382820512568442930 
        log_channel = self.bot.get_channel(log_channel_id)
        
        if not log_channel:
            print(f'❌ Canal de logs não encontrado! ID usado: {log_channel_id}')
            return
        
        print(f'📨 Enviando log para o canal: #{log_channel.name}')
        
    
        embed = Embed(
                title = '⚠️ Mensagem Excluída',
                description = f'Mensagem de {message.author.mention} excluída em {message.channel.mention}',
                color = Color.red()
            )
        embed.add_field(name='Conteúdo', value=message.content or '[Sem conteúdo]')
            
        await log_channel.send(embed=embed)
        print('✅ Mensagem de log enviada com sucesso!')
        

def setup(bot: Bot):
    bot.add_cog(MessageDelete(bot))
    print('MemberRemove cog loaded successfully.') 