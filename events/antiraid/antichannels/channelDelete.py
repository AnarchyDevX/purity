from discord.ext import commands
from functions.functions import *
import discord
import json
from core.embedBuilder import embedBuilder

class guildChannelDeleteAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if channel.guild.id in getattr(self.bot, "_backup_loading_guilds", set()):
            return
        guildJSON = load_json_file(f"./configs/{channel.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        config = load_json()
        if guildJSON['antiraid']['channels']['delete'] == True:
            async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_delete):
                time_diff = (discord.utils.utcnow() - entry.created_at).total_seconds()
                if time_diff > 5:  # Ignorer les entries anciennes
                    continue
                    
                if entry.target.id == channel.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if await check_id_perms(entry.user, entry.user.guild, 2): return

                    try:
                        await entry.user.ban(reason="Antiraid: Salon Supprimé")
                    except discord.Forbidden:
                        return
                    except discord.HTTPException:
                        return
                    break

async def setup(bot):
    await bot.add_cog(guildChannelDeleteAntiraid(bot))