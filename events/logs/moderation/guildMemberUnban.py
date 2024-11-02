from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class guildMemberUnban(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        logsChannel = await check_if_logs(guild, 'modlogs')
        if logsChannel:
            embed = embedBuilder(
                description=f"```[{time_now()}] - Mods | Membre débanni```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations sur le membre débanni:": (
                        f"> `🪄`・**Nom:** `{user.name}`\n"
                        f"> `🆔`・**Id:** `{user.id}`\n"
                        f"> `✨`・**Mention:** {user.mention}\n"
                        f"> `🔨`・**Créé le:** `{format_date('all', user.created_at)}`",
                        False
                    )
                }
            )
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
                if entry.target.id == user.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if entry.user:
                        embed.add_field(
                            name="`✨`・Informations sur le débannisseur:",
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
    await bot.add_cog(guildMemberUnban(bot))