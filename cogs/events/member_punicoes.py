import discord
from discord import Member, Embed, Color, Guild, User
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands import Cog
from datetime import datetime, timedelta
from discord import AuditLogAction

class LogCastigar(Cog):
        def __init__(self, bot):
            self.bot = bot
            self.log_channel_id = 1382821037099581622 

        def get_log_channel(self):
            return self.bot.get_channel(self.log_channel_id)

        @Cog.listener('on_member_ban')
        async def on_member_ban(self, guild: Guild, user: User):
            log_channel = self.get_log_channel()
            if not log_channel:
                return

            # Busca quem baniu (última entrada do log de auditoria)
            reason = "Sem motivo"
            moderator = "Desconhecido"

            try:
                entry = await guild.audit_logs(action=discord.AuditLogAction.ban).get()
                if entry and entry.target == user:
                    moderator = entry.user
                    reason = entry.reason or "Sem motivo"
            except:
                pass

            embed = Embed(
                title="⛔ Membro Banido",
                description=f"{user.mention} foi banido.",
                color=Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Moderador", value=moderator.mention)
            embed.add_field(name="Motivo", value=reason)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)

            await log_channel.send(embed=embed)

        @Cog.listener('on_member_unban')
        async def on_member_unban(self, guild: Guild, user: discord.User):
            log_channel = self.get_log_channel()
            if not log_channel:
                return

            # Busca quem desbaniu
            reason = "Sem motivo"
            moderator = "Desconhecido"

            try:
                entry = await guild.audit_logs(action=discord.AuditLogAction.unban).get()
                if entry and entry.target == user:
                    moderator = entry.user
                    reason = entry.reason or "Sem motivo"
            except:
                pass

            embed = Embed(
                title="✅ Membro Desbanido",
                description=f"{user.mention} foi desbanido.",
                color=Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Moderador", value=moderator.mention)
            embed.add_field(name="Motivo", value=reason)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)

            await log_channel.send(embed=embed)

        @Cog.listener('on_member_remove')
        async def on_member_remove(self, member: Member):
            log_channel = self.get_log_channel()
            if not log_channel:
                return

            # Verifica se foi kick ou saída normal
            reason = "Saiu do servidor"
            moderator = "Desconhecido"

            try:
                entry = await member.guild.audit_logs(action=discord.AuditLogAction.kick).get()
                if entry and entry.target.id == member.id:
                    moderator = entry.user
                    reason = entry.reason or "Sem motivo"
            except:
                pass

            embed = Embed(
                title="👢 Membro Expulso",
                description=f"{member.mention} foi expulso.",
                color=Color.orange(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Moderador", value=moderator.mention)
            embed.add_field(name="Motivo", value=reason)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)

            await log_channel.send(embed=embed)




def setup(bot):
    bot.add_cog(LogCastigar(bot))




