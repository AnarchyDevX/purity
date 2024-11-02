from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildRoleCreate(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        logsChannel = await check_if_logs(role.guild, "raidlogs")
        if logsChannel:
            embed = embedBuilder(
                description=f"```[{time_now()}] - Raid | Role Créé```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations sur le rôle": (
                        f"> `🪄`・**Nom:** `{role.name}`\n"
                        f"> `✨`・**Mention:** {role.mention}\n"
                        f"> `🆔`・**Id:** `{role.id}`\n"
                        f"> `➕`・**Position:** `{role.position}`\n"
                        f"> `🛠️`・**Couleur:** `{role.color}`\n", 
                        False
                    ),
                }
            )
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                if entry.target.id == role.id:
                    if entry.user.id == self.bot.user.id:
                        return 
                    embed.add_field(
                        name="`✨`・Informations sur le créateur du rôle",
                        value=(
                            f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                            f"> `🆔`・**Id:** `{entry.user.id}`\n"
                            f"> `✨`・**Mention:** {entry.user.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', entry.user.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', entry.user.joined_at)}`"
                        ),
                        inline=False
                    )
                    break

            await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(guildRoleCreate(bot))
