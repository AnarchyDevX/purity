from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class voiceDeafed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id:
            return
        logsChannel = await check_if_logs(member.guild, 'voicelogs')
        if logsChannel:
            if before.deaf == False and after.deaf == True:
                embed = embedBuilder(
                    description=f"```[{time_now()}] - Voice | Mis En Sourdine```",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`🪡`・Informations sur le membre:": (
                            f"> `🪄`・**Nom:** `{member.name}`\n"
                            f"> `🆔`・**Id:** `{member.id}`\n"
                            f"> `✨`・**Mention:** {member.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', member.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', member.joined_at)}`",
                            f"> `📜`・**Salon de l'action:** {after.channel.mention}",
                            False
                        ),
                    }
                )
                async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                    if entry.target.id == member.id and entry.changes.after.deaf:
                        embed.add_field(
                            name="`✨`・Informations sur le modérateur:",
                            value=(
                                f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                                f"> `🆔`・**Id:** `{entry.user.id}`\n"
                                f"> `✨`・**Mention:** {entry.user.mention}\n"
                                f"> `📜`・**Raison:** ```{entry.reason if entry.reason else 'pas de raison fournie'}```"
                            ),
                            inline=False
                        )
                        break
                await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(voiceDeafed(bot))