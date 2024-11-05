import discord
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class guildChannelCreateAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        guildJSON = load_json_file(f"./configs/{channel.guild.id}.json")
        if guildJSON['antiraid']['channels']['create'] == True:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                if entry.target.id == channel.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if await check_id_perms(entry.user, entry.user.guild, 2): return

                    try:
                        await channel.delete(reason="Antiraid: Salon Créé")
                        await entry.user.ban(reason="Antiraid: Salon Créé")
                    except Exception: return
                    break

async def setup(bot):
    await bot.add_cog(guildChannelCreateAntiraid(bot))