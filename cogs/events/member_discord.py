from enum import member
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog
import os
from discord import Message, Embed, Color
from datetime import datetime
from discord import Member, AuditLogAction

class LogDiscord(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1382820329684078603  # Substitua pelo ID real do seu canal de logs

    def get_log_channel(self):
        return self.bot.get_channel(self.log_channel_id)

    async def get_audit_log_entry(self, guild, action_type):
        """Busca a última entrada do log de auditoria"""
        try:
            entry = await guild.audit_logs(action=action_type).get()
            return entry
        except:
            return None

    @Cog.listener('on_member_update')
    async def on_member_update(self, before: Member, after: Member):
        # Ignorar se os cargos não mudaram
        if before.roles == after.roles:
            return

        # Detectar cargos adicionados/removidos
        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]

        log_channel = self.get_log_channel()
        if not log_channel:
            print("❌ Canal de logs não encontrado.")
            return

        guild = before.guild

        # Registrar adição de cargos
        if added_roles:
            for role in added_roles:
                # Buscar moderador via log de auditoria
                entry = await self.get_audit_log_entry(guild, AuditLogAction.member_role_update)

                moderator = None
                reason = "Sem motivo"

                if entry and entry.target.id == after.id:
                    moderator = entry.user
                    reason = entry.reason or "Sem motivo"

                embed = Embed(
                    title="🟢 Adicionou cargo",
                    description=f"{after.mention} recebeu o cargo {role.mention}",
                    color=Color.green(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="Moderador", value=moderator.mention if moderator else "Desconhecido")
                embed.add_field(name="Motivo", value=reason, inline=False)

                await log_channel.send(embed=embed)

        # Registrar remoção de cargos
        if removed_roles:
            for role in removed_roles:
                # Buscar moderador via log de auditoria
                entry = await self.get_audit_log_entry(guild, AuditLogAction.member_role_update)

                moderator = None
                reason = "Sem motivo"

                if entry and entry.target.id == after.id:
                    moderator = entry.user
                    reason = entry.reason or "Sem motivo"

                embed = Embed(
                    title="🔴 Removeu cargo",
                    description=f"{after.mention} perdeu o cargo {role.mention}",
                    color=Color.red(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="Moderador", value=moderator.mention if moderator else "Desconhecido")
                embed.add_field(name="Motivo", value=reason, inline=False)

                await log_channel.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(LogDiscord(bot))

