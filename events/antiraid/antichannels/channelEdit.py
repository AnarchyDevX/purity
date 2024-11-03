import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildChannelUpdateAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        guildJSON = load_json_file(f"./configs/{before.guild.id}.json")
        if guildJSON['antiraid']['channels']['edit'] == True:
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
                if entry.target.id == before.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if not await check_id_perms(entry.user, entry.user.guild, 2): return

                    try: await entry.user.ban(reason="Antiraid: Salon Modifié")
                    except Exception: return
                    break

async def setup(bot):
    await bot.add_cog(guildChannelUpdateAntiraid(bot))