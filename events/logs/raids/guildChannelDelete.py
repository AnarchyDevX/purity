from discord.ext import commands
from functions.functions import *
import discord
import json
from core.embedBuilder import embedBuilder

class guildChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        logsChannel = await check_if_logs(channel.guild, 'raidlogs')
        if logsChannel:
            embed = embedBuilder(
                description=f"```[{time_now()}] - Raid | Salon Supprimé```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Informations sur le salon": (
                        f"> `🪄`・**Nom:** `{channel.name}`\n"
                        f"> `🆔`・**Id:** `{channel.id}`\n"
                        f"> `➕`・**Position:** `{channel.position}`\n"
                        f"> `🛠️`・**Type:** `{channel.type}`\n",
                        False
                    )
                }
            )
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                if entry.target.id == channel.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    embed.add_field(
                        name="`✨`・Informations sur le modérateur",
                        value=(
                            f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                            f"> `🆔`・**Id:** `{entry.user.id}`\n"
                            f"> `✨`・**Mention:** {entry.user.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', entry.user.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all',  entry.user.joined_at)}`"
                        ),
                        inline=False
                    )
                    break
            try:
                await logsChannel.send(embed=embed)
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                pass

async def setup(bot):
    await bot.add_cog(guildChannelDelete(bot))