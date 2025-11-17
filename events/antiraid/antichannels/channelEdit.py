import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildChannelUpdateAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if before.guild.id in getattr(self.bot, "_backup_loading_guilds", set()):
            return
        guildJSON = load_json_file(f"./configs/{before.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        if guildJSON['antiraid']['channels']['edit'] == True:
            async for entry in before.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_update):
                time_diff = (discord.utils.utcnow() - entry.created_at).total_seconds()
                if time_diff > 5:  # Ignorer les entries anciennes
                    continue
                    
                if entry.target.id == before.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if await check_id_perms(entry.user, entry.user.guild, 2): return

                    try:
                        await entry.user.ban(reason="Antiraid: Salon Modifié")
                    except discord.Forbidden:
                        return
                    except discord.HTTPException:
                        return
                    break

async def setup(bot):
    await bot.add_cog(guildChannelUpdateAntiraid(bot))