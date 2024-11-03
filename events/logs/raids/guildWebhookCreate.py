import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildWebhookCreate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel):
        logsChannel: discord.abc.GuildChannel | None = await check_if_logs(channel.guild, 'raidlogs') 
        if logsChannel:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create):
                if isinstance(entry.target, discord.Webhook) and getattr(entry.target, 'channel', None):
                    if entry.target.channel.id == channel.id:
                        if entry.user.id == self.bot.user.id:
                            return
                        embed: embedBuilder = embedBuilder(
                            description=f"```[{time_now()}] - Raid | Webhook Crée```",
                            color=embed_color(),
                            footer=footer(),
                            fields={
                                "`🪡`・Informations sur le créateur": (
                                    f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                                    f"> `🆔`・**Id:** `{entry.user.id}`\n"
                                    f"> `✨`・**Mention:** {entry.user.mention}\n"
                                    f"> `🔨`・**Créé le:** `{format_date('all', entry.user.created_at)}`\n"
                                    f"> `➕`・**Rejoint le:** `{format_date('all', entry.user.joined_at)}`\n",
                                    False
                                ),
                                "`✨`・Informations sur le webhook": (
                                    f"> `🪄`・**Nom:** `{entry.target.name}`\n"
                                    f"> `🆔`・**Id:** `{entry.target.id}`\n"
                                    f"> `✨`・**Token:** `{entry.target.auth_token}`\n"
                                    f"> `🔨`・**Créé le:** `{format_date('all', entry.target.created_at)}`\n"
                                    f"> `🛠️`・**Channel:** {entry.target.channel.mention}\n",
                                    False
                                )
                            }
                        )
                        await logsChannel.send(embed=embed)
                        break

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(guildWebhookCreate(bot))
