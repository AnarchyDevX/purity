import discord
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class botJoin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if not member.bot:
            return
        logsChannel: discord.abc.GuildChannel | None = await check_if_logs(member.guild, "raidlogs")
        if logsChannel:
            embed: embedBuilder = embedBuilder(
                description=f"```[{time_now()}] - Raid | Bot Ajouté```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations sur le bot": (
                        f"> `🪄`・**Nom:** `{member.name}`\n"
                        f"> `🆔`・**Id:** `{member.id}`\n"
                        f"> `✨`・**Mention:** {member.mention}\n"
                        f"> `🔨`・**Créé le:** `{format_date('all', member.created_at)}`\n"
                        f"> `➕`・**Rejoint le:** `{format_date('all', member.joined_at)}`\n",
                        False
                    )
                }
            )
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                if entry.target.id == member.id:
                    embed.add_field(
                        name=f"`✨`・Informations sur le membre ayant ajouté le bot",
                        value=(
                            f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                            f"> `🆔`・**Id:** `{entry.user.id}`\n"
                            f"> `✨`・**Mention:** {entry.user.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', entry.user.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', entry.user.joined_at)}`\n"
                        )
                    )
            await logsChannel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(botJoin(bot))