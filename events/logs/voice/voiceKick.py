import discord
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class voiceKicked(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id:
            return
        logsChannel = await check_if_logs(member.guild, 'voicelogs')
        if logsChannel:
            if before.channel != after.channel and before.channel != None and after.channel == None:
                async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_disconnect):
                    embed = embedBuilder(
                        description=f"```[{time_now()}] - Voice | Membre Expulser```",
                        color=embed_color(),
                        footer=footer(),
                        fields={
                            "`🪡`・Informations sur le membre:": (
                                f"> `🪄`・**Nom:** `{member.name}`\n"
                                f"> `🆔`・**Id:** `{member.id}`\n"
                                f"> `✨`・**Mention:** {member.mention}\n"
                                f"> `🔨`・**Créé le:** `{format_date('all', member.joined_at)}`\n"
                                f"> `➕`・**Rejoint le:** `{format_date('all', member.created_at)}`\n"
                                f"> `📜`・**Salon de l'action:** {before.channel.mention}", 
                                False
                            ),
                            "`✨`・Informations sur le modérateur:": (
                                f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                                f"> `🆔`・**Id:** `{entry.user.id}`\n"
                                f"> `✨`・**Mention:** {entry.user.mention}\n"
                                f"> `🔨`・**Créé le:** `{format_date('all', entry.user.joined_at)}`\n"
                                f"> `➕`・**Rejoint le:** `{format_date('all', entry.user.joined_at)}`\n", 
                                False
                            ),
                            "`🛠️`・Informations sur l'expulsion:": (
                                f"> `⚙️`・**Ancien Salon:** {before.channel.mention}\n", 
                                False
                            ),
                        }
                    )
                    await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(voiceKicked(bot))