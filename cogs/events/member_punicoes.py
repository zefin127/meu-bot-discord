import discord
from discord.ext import commands

# Ativar intents necessários
intents = discord.Intents.default()
intents.moderation = True  # Para bans/expulsões
intents.guilds = True
intents.members = True

# Inicializar o bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ID do canal de logs
LOG_CHANNEL_ID = 1382821037099581622  # ← Substitua pelo ID real do seu canal de logs


@bot.event
async def on_ready():
    print(f"Bot está online como {bot.user}")
    await bot.sync_commands()  # Sincroniza os comandos slash


@bot.slash_command(name="kick", description="Expulsa um membro do servidor")
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, motivo: str = "Nenhum motivo fornecido"):
    if membro.top_role >= ctx.author.top_role:
        await ctx.respond("Você não pode expulsar alguém com cargo igual ou superior ao seu.")
        return

    try:
        await membro.kick(reason=motivo)
        await ctx.respond(f"{membro.mention} foi expulso por {ctx.author.mention} | Motivo: {motivo}")

        # Log no canal de logs
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="👢 Membro Expulso",
                description=f"{membro.mention} foi expulso por {ctx.author.mention}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Motivo", value=motivo)
            await log_channel.send(embed=embed)

    except discord.Forbidden:
        await ctx.respond("Não tenho permissão para expulsar esse membro.")
    except Exception as e:
        await ctx.respond(f"Erro ao expulsar: {e}")


@bot.slash_command(name="ban", description="Bane um membro do servidor")
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, motivo: str = "Nenhum motivo fornecido"):
    if membro.top_role >= ctx.author.top_role:
        await ctx.respond("Você não pode banir alguém com cargo igual ou superior ao seu.")
        return

    try:
        await membro.ban(reason=motivo)
        await ctx.respond(f"{membro.mention} foi banido por {ctx.author.mention} | Motivo: {motivo}")

        # Log no canal de logs
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="⛔ Membro Banido",
                description=f"{membro.mention} foi banido por {ctx.author.mention}",
                color=discord.Color.red()
            )
            embed.add_field(name="Motivo", value=motivo)
            await log_channel.send(embed=embed)

    except discord.Forbidden:
        await ctx.respond("Não tenho permissão para banir esse membro.")
    except Exception as e:
        await ctx.respond(f"Erro ao banir: {e}")


@bot.slash_command(name="unban", description="Desbane um usuário pelo ID")
@commands.has_permissions(ban_members=True)
async def unban(ctx, usuario_id: str, motivo: str = "Nenhum motivo fornecido"):
    try:
        user = await bot.fetch_user(int(usuario_id))
        await ctx.guild.unban(user, reason=motivo)
        await ctx.respond(f"{user.mention} foi desbanido.")

        # Log no canal de logs
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="✅ Membro Desbanido",
                description=f"{user.mention} foi desbanido por {ctx.author.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Motivo", value=motivo)
            await log_channel.send(embed=embed)

    except discord.NotFound:
        await ctx.respond("Usuário não encontrado ou não está banido.")
    except discord.Forbidden:
        await ctx.respond("Não tenho permissão para desbanir.")
    except ValueError:
        await ctx.respond("ID inválido. Forneça um número válido.")
    except Exception as e:
        await ctx.respond(f"Erro ao desbanir: {e}")

