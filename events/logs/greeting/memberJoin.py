import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class memberJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logsChannel: discord.abc.GuildChannel | None = await check_if_logs(member.guild, "joinleavelogs")
        if logsChannel:
            embed: embedBuilder = embedBuilder(
                description=f"```[{time_now()}] - Membre | Arrivée```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations sur le membre": (
                        f"> `🪄`・**Nom:** `{member.name}`\n"
                        f"> `🆔`・**Id:** `{member.id}`\n"
                        f"> `✨`・**Mention:** {member.mention}\n"
                        f"> `🔨`・**Créé le:** `{format_date('all', member.created_at)}`\n"
                        f"> `➕`・**Rejoint le:** `{format_date('all', member.joined_at)}`\n",
                        False
                    ),
                }
            )
            await logsChannel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(memberJoin(bot))