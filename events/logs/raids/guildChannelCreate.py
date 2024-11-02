import discord
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class guildChannelCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        logsChannel = await check_if_logs(channel.guild, "raidlogs")
        if logsChannel:
            embed = embedBuilder(
                description=f"```[{time_now()}] - Raid | Salon Créé```",
                footer=footer(),
                color=embed_color(),
                fields={
                    "`🪡`・Informations sur le salon": (
                        f"> `🪄`・**Nom:** `{channel.name}`\n"
                        f"> `✨`・**Mention:** {channel.mention}\n  "
                        f"> `🆔`・**Id:** `{channel.id}`\n"
                        f"> `➕`・**Position:** `{channel.position}`\n"
                        f"> `🛠️`・**Type:** `{channel.type}`\n",
                        False
                    )
                }
            )
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
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
                            f"> `➕`・**Rejoint le:** `{format_date('all', entry.user.joined_at)}`"
                        ),
                        inline=False
                    )
                    break
            await logsChannel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(guildChannelCreate(bot))