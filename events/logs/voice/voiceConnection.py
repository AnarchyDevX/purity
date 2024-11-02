import json
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class voiceConnection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id:
            return
        logsChannel = await check_if_logs(member.guild, 'voicelogs')
        if logsChannel:
            if before.channel == None and after.channel != None:
                embed = embedBuilder(
                    description=f"```[{time_now()}] - Logs | Connection dans un Salon```",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`🪡`・Informations sur le membre:": (
                            f"> `🪄`・**Nom:** `{member.name}`\n"
                            f"> `🆔`・**Id:** `{member.id}`\n"
                            f"> `✨`・**Mention:** {member.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', member.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', member.joined_at)}`",
                            False
                        ),
                        "`✨`・Informations sur le salon vocal:": (
                            f"> `🪄`・**Mention:** {after.channel.mention}\n"
                            f"> `🆔`・**Id:** `{after.channel.id}`\n"
                            f"> `🛠️`・**Position:** `{after.channel.position}`\n"
                            f"> `👤`・**Membres Connectés:** `{len(after.channel.members)}`\n",
                            False
                        ),
                    }
                )
                await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(voiceConnection(bot))