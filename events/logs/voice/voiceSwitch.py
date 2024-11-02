from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class voiceSwitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id:
            return
        logsChannel = await check_if_logs(member.guild, 'voicelogs')
        if logsChannel:
            toCheck = [ 'mute', 'deaf', 'self_deaf', 'self_mute', 'self_stream', 'self_video']
            if before.channel is not None and after.channel is not None:
                if any(getattr(before, attr) != getattr(after, attr) for attr in toCheck):
                    return
                embed = embedBuilder(
                    description=f"```[{time_now()}] - Voice | Changement de Salon```",
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
                        "`✨`・Informations sur l'ancien salon vocal:": (
                            f"> `🪄`・**Mention:** {before.channel.mention}\n"
                            f"> `🆔`・**Id:** `{before.channel.id}`\n"
                            f"> `🛠️`・**Position:** `{before.channel.position}`\n"
                            f"> `👤`・**Membres Connectés:** `{len(before.channel.members)}`\n",
                            False
                        ),
                        "`✨`・Informations sur le nouveau salon vocal:": (
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
    await bot.add_cog(voiceSwitch(bot))