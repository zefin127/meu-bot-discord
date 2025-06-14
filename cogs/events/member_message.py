import discord

intents = discord.Intents.default()
intents.message_content = True  # Necessário para acessar conteúdo de mensagens
intents.guilds = True
intents.messages = True  # Para detectar exclusão de mensagens
intents.members = True  # Para acessar informações de membros

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot está online como {bot.user}")

@bot.event
async def on_message_delete(message: discord.Message):
    print("[DEBUG] Evento on_message_delete disparado!")  # ← Verifica se o evento foi chamado
    
    if message.author.bot:
        print("⚠️ Mensagem ignorada: é de um bot.")
        return
    
    print(f"👤 Autor da mensagem: {message.author}")
    print(f"📢 Canal onde a mensagem foi apagada: #{message.channel.name}")
    print(f"📄 Conteúdo da mensagem excluída: {message.content}")
    
    log_channel_id = 1382820512568442930 
    log_channel = bot.get_channel(log_channel_id)
    
    if not log_channel:
        print(f"❌ Canal de logs não encontrado! ID usado: {log_channel_id}")
        return
    
    print(f"📨 Enviando log para o canal: #{log_channel.name}")
    
 
    embed = discord.Embed(
            title="⚠️ Mensagem Excluída",
            description=f"Mensagem de {message.author.mention} excluída em {message.channel.mention}",
            color=discord.Color.red()
        )
    embed.add_field(name="Conteúdo", value=message.content or "[Sem conteúdo]")
        
    await log_channel.send(embed=embed)
    print("✅ Mensagem de log enviada com sucesso!")
    
