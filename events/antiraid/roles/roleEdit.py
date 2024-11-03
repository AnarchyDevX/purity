import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildRoleUpdateAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        guildJSON = load_json_file(f"./configs/{before.guild.id}.json")
        if guildJSON['antiraid']['roles']['edit'] == True:
            if before.position != after.position:
                return
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
                if entry.target.id == before.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if not await check_id_perms(entry.user, entry.user.guild, 2): return
                    try: await entry.user.ban(reason="Antiraid: Role Modifié")
                    except Exception: pass
                    try:
                        await after.edit(
                            name=before.name,
                            permissions=before.permissions,
                            colour=before.colour,
                            color=before.color,
                            hoist=before.hoist,
                            display_icon=before.display_icon,
                            mentionable=before.mentionable,
                            position=before.position
                        )
                    except Exception: return
                    break

async def setup(bot):
    await bot.add_cog(guildRoleUpdateAntiraid(bot))