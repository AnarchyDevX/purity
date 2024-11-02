from discord.ext import commands
from functions.functions import *
import json
from typing import Optional
from core.embedBuilder import embedBuilder

class roleDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.id == self.bot.user.id:
            return
        logsChannel: Optional[discord.abc.GuildChannel] = await check_if_logs(before.guild, 'ranklogs')
        if logsChannel:
            newRole: Optional[discord.Role] = next((role for role in before.roles if role not in after.roles), None)
            if newRole:
                embed: discord.Embed = embedBuilder(
                    description=f"```[{time_now()}] - Roles | Role Retiré```",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`🪡`・Informations sur le membre:": (
                            f"> `🪄`・**Nom:** `{after.name}`\n"
                            f"> `🆔`・**Id:** `{after.id}`\n"
                            f"> `✨`・**Mention:** {after.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', after.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', after.joined_at)}`",
                            False
                        ),
                        "`🛠️`・Changement des roles:": (
                            f"> `🎯`・**Rôle retiré:** {newRole.mention}",
                            False
                        )
                    }
                )
                await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(roleDown(bot))