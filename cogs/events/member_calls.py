import discord

intents = discord.Intents.default()
intents.voice_states = True  # Necessário para detectar mudanças nos estados de voz
intents.guilds = True
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot está online como {bot.user}")

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # Ignorar bots (opcional)
    if member.bot:
        return

    log_channel_id = 1382820759608496178  # Substitua pelo ID do seu canal de logs
    log_channel = bot.get_channel(log_channel_id)

    # Verifica se o canal existe
    if not log_channel:
        print("❌ Canal de logs não encontrado.")
        return

    # Entrou em um canal de voz
    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            title="🟢 Entrou no canal de voz",
            description=f"{member.mention} entrou no canal **{after.channel.name}**",
            color=discord.Color.green()
        )
        await log_channel.send(embed=embed)

    # Saiu de um canal de voz
    elif before.channel is not None and after.channel is None:
        embed = discord.Embed(
            title="🔴 Saiu do canal de voz",
            description=f"{member.mention} saiu do canal **{before.channel.name}**",
            color=discord.Color.red()
        )
        await log_channel.send(embed=embed)

    # Mudou de canal de voz
    elif before.channel != after.channel:
        embed = discord.Embed(
            title="🟡 Trocou de canal de voz",
            description=f"{member.mention} foi de **{before.channel.name}** para **{after.channel.name}**",
            color=discord.Color.orange()
        )
        await log_channel.send(embed=embed)

    # Mute ou deaf foi alterado
    elif before.mute != after.mute or before.deaf != after.deaf:
        action = []
        if before.mute != after.mute:
            action.append("Microfone mutado" if after.mute else "Microfone desmutado")
        if before.deaf != after.deaf:
            action.append("Fone mutado" if after.deaf else "Fone desmutado")

        embed = discord.Embed(
            title="🔵 Atualização no status de áudio",
            description=f"{member.mention}: {', '.join(action)}",
            color=discord.Color.blue()
        )
        await log_channel.send(embed=embed)

