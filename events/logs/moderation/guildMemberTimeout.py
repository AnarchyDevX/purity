import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildMemberTimeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.id == self.bot.user.id:
            return
        logsChannel = await check_if_logs(before.guild, 'modlogs')
        if logsChannel:
            if before.is_timed_out() == False and after.is_timed_out() == True:                
                embed = embedBuilder(
                    description=f"```[{time_now()}] - Mods | Membre Rendu Muet```",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`🪡`・Informations sur le membre muet": (
                            f"> `🪄`・**Nom:** `{after.name}`\n"
                            f"> `🆔`・**Id:** `{after.id}`\n"
                            f"> `✨`・**Mention:** {after.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', before.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', before.joined_at)}`",
                            False
                        )
                    }
                )
                await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(guildMemberTimeout(bot))