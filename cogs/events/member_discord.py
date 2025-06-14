import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Configuração dos intents
intents = discord.Intents.default()
intents.moderation = True  # Necessário para acessar logs de auditoria

# Inicialização do bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ID do canal onde os logs serão enviados
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))  # Substitua no .env

@bot.event
async def on_ready():
    print(f"✅ Bot está online como {bot.user}")

def format_action(action: discord.AuditLogAction):
    """Formata a ação do log de auditoria"""
    return str(action).replace("AuditLogAction.", "").upper()

@bot.event
async def on_audit_log_entry(entry: discord.AuditLogEntry):
    """
    Chamado quando uma entrada de log de auditoria é criada.
    Apenas se o autor estiver em cache.
    """
    print(f"[on_audit_log_entry] Nova ação detectada: {entry.action}")
    
    if LOG_CHANNEL_ID == 0:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    action = format_action(entry.action)
    user = entry.user or "Desconhecido"
    target = entry.target or "Desconhecido"
    reason = entry.reason or "Sem motivo"

    embed = discord.Embed(
        title=f"📜 Ação de Moderação: {action}",
        color=discord.Color.orange()
    )
    embed.add_field(name="👮 Autor", value=f"{user} ({user.id})" if isinstance(user, discord.User) else user, inline=False)
    embed.add_field(name="🎯 Alvo", value=str(target), inline=False)
    embed.add_field(name="📝 Motivo", value=reason, inline=False)
    embed.set_footer(text=f"ID da ação: {entry.id}")

    try:
        await log_channel.send(embed=embed)
    except discord.Forbidden:
        print("❌ O bot não tem permissão para enviar mensagens no canal de logs.")
    except Exception as e:
        print(f"⚠️ Erro ao enviar mensagem no canal de logs: {e}")


@bot.event
async def on_raw_audit_log_entry(payload: discord.RawAuditLogEntryEvent):
    """
    Chamado com dados brutos de entrada de log de auditoria.
    Funciona mesmo sem cache do usuário.
    """
    print(f"[on_raw_audit_log_entry] Nova ação BRUTA detectada: {payload.action}")

    if LOG_CHANNEL_ID == 0:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    action = format_action(payload.action)
    user_id = payload.user_id
    reason = payload.reason or "Sem motivo"

    embed = discord.Embed(
        title=f"📦 Ação Bruta de Moderação: {action}",
        color=discord.Color.dark_orange()
    )
    embed.add_field(name="👮 ID do Autor", value=user_id or "Desconhecido", inline=False)
    embed.add_field(name="🎯 ID do Alvo", value=payload.target_id or "Desconhecido", inline=False)
    embed.add_field(name="📝 Motivo", value=reason, inline=False)

    try:
        await log_channel.send(embed=embed)
    except discord.Forbidden:
        print("❌ O bot não tem permissão para enviar mensagens no canal de logs.")
    except Exception as e:
        print(f"⚠️ Erro ao enviar mensagem no canal de logs: {e}")

