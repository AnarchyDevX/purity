from functions.functions import *
from discord.ext import commands
from typing import Union
from core.embedBuilder import embedBuilder

class guildMemberBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: Union[discord.User, discord.Member]):
        logsChannel = await check_if_logs(guild, 'modlogs')
        if logsChannel:
            date = format_date('all', member.joined_at) if member.joined_at != None else 'non determiné'
            embed = embedBuilder(
                description=f"```[{time_now()}] - Mods | Membre Banni```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations sur le membre banni:": (
                        f"> `🪄`・**Nom:** `{member.name}`\n"
                        f"> `🆔`・**Id:** `{member.id}`\n"
                        f"> `✨`・**Mention:** {member.mention}\n"
                        f"> `🔨`・**Créé le:** `{format_date('all', member.created_at)}`\n"
                        f"> `➕`・**Rejoint le:** `{date}`",
                        False
                    ),
                }
            )
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                if entry.target.id == member.id:
                    raison = entry.reason if entry.reason != None else "pas de raison fournie"
                    embed.add_field(
                        name="`✨`・Informations sur le bannisseur:",
                        value=(
                            f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                            f"> `🆔`・**Id:** `{entry.user.id}`\n"
                            f"> `✨`・**Mention:** {entry.user.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', entry.user.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', entry.user.joined_at)}`"
                        ),
                        inline=False
                    )
                    embed.add_field(
                        name="`📜`・Informations sur le bannissement:",
                        value=(
                            f"> `🕐`・**Heure:** `{time_now()}`\n"
                            f"> `❓`・**Raison:** \n"
                            f"```{raison}```"
                        ),
                        inline=False
                    )
                    break
            await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(guildMemberBan(bot))