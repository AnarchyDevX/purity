from discord.ext import commands
from functions.functions import *
import json
from typing import Optional
from core.embedBuilder import embedBuilder

class roleDownAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.id == self.bot.user.id:
            return
        guildJSON = load_json_file(f"./configs/{before.guild.id}.json")
        if guildJSON['antiraid']["rank"]["down"] == True:
            newRole: Optional[discord.Role] = next((role for role in after.roles if role not in before.roles), None)
            if newRole:
                async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                    if entry.target.id == after.id:
                        if await check_id_perms(entry.user, entry.user.guild, 2): return
                        try: await entry.user.ban(reason="Antiraid: Rank Down")
                        except Exception: pass
                        try: await after.add_roles(newRole)
                        except: return
async def setup(bot):
    await bot.add_cog(roleDownAntiraid(bot))