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
        guildJSON = load_json_file(f"./configs/{channel.guild.id}.json")
        config = load_json()
        if guildJSON['antiraid']['channels']['delete'] == True:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                if entry.target.id == channel.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if not await check_id_perms(entry.user, entry.user.guild, 2): return

                    try: await entry.user.ban(reason="Antiraid: Salon Supprimé")
                    except Exception: return
                    break

async def setup(bot):
    await bot.add_cog(guildChannelDeleteAntiraid(bot))