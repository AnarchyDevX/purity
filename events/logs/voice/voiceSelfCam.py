from discord.ext import commands
from functions.functions import *
import json
from core.embedBuilder import embedBuilder

class voiceSelfCam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id:
            return
        logsChannel = await check_if_logs(member.guild, 'voicelogs')
        if logsChannel:
            if before.self_video == False and after.self_video == True:
                embed = embedBuilder(
                    description=f"```[{time_now()}] - Voice | Caméra Activée```",
                    color=embed_color(),
                    footer=footer(),
                    fieds={
                        "`🪡`・Informations sur le membre:": (
                            f"> `🪄`・**Nom:** `{member.name}`\n"
                            f"> `🆔`・**Id:** `{member.id}`\n"
                            f"> `✨`・**Mention:** {member.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', member.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', member.joined_at)}`\n"
                            f"> `📜`・**Salon de l'action:** {after.channel.mention}", 
                            False
                        ),
                    }
                )
                await logsChannel.send(embed=embed)
                
async def setup(bot):
    await bot.add_cog(voiceSelfCam(bot))