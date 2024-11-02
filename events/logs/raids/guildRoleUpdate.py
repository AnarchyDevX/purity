import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildRoleUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        logsChannel = await check_if_logs(before.guild, "raidlogs")
        if logsChannel:
            if before.position != after.position:
                return
            embed = embedBuilder(
                description=f"```[{time_now()}] - Raid | Role Modifié```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations avant la modification": (
                        f"> `🪄`・**Nom:** `{before.name}`\n"
                        f"> `🆔`・**Id:** `{before.id}`\n"
                        f"> `➕`・**Position:** `{before.position}`\n"
                        f"> `🛠️`・**Couleur:** `{before.color}`\n",
                        False
                    ),
                    "`🪄`・Informations après la modification": (
                        f"> `🪄`・**Nom:** `{after.name}`\n"
                        f"> `🆔`・**Id:** `{after.id}`\n"
                        f"> `➕`・**Position:** `{after.position}`\n"
                        f"> `🛠️`・**Couleur:** `{after.color}`\n",
                        False
                    ),
                    "`🛠️`・Informations utiles": (
                        f"> `💈`・**Mention:** {after.mention}\n",
                        False
                    )
                }
            )
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
                if entry.target.id == before.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    embed.add_field(
                        name="`✨`・Informations sur le modérateur",
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
    await bot.add_cog(guildRoleUpdate(bot))