from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog
from datetime import datetime 

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
                color = Color.red(),
                timestamp=datetime.now()
            )
        embed.add_field(name='Conteúdo', value=message.content or '[Sem conteúdo]')
            
        await log_channel.send(embed=embed)
        print('✅ Mensagem de log enviada com sucesso!')

    @Cog.listener('on_message_edit')
    async def message_edit(self, before: Message, after: Message):
        if before.author.bot:
            return

        if before.content == after.content:
            return  # Ignorar se o conteúdo não mudou

        print(f'✏️ Mensagem editada por: {before.author}')
        print(f'📢 Canal: #{before.channel.name}')
        print(f'🔍 Antes: {before.content}')
        print(f'📝 Depois: {after.content}')

        log_channel_id = 1382820512568442930
        log_channel = self.bot.get_channel(log_channel_id)

        if not log_channel:
            print(f'❌ Canal de logs não encontrado! ID usado: {log_channel_id}')
            return

        print(f'📨 Enviando log de edição para o canal: #{log_channel.name}')

        embed = Embed(
            title='✏️ Mensagem Editada',
            description=f'Mensagem de {before.author.mention} editada em {before.channel.mention}',
            color=Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name='Antes', value=before.content or '[Sem conteúdo]', inline=False)
        embed.add_field(name='Depois', value=after.content or '[Sem conteúdo]', inline=False)

        await log_channel.send(embed=embed)
        print('✅ Mensagem de edição registrada no log!')

        
        

def setup(bot: Bot):
    bot.add_cog(MessageDelete(bot))
