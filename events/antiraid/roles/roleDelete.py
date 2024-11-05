from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildRoleDeleteAntiraid(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        config = load_json()
        guildJSON = load_json_file(f"./configs/{role.guild.id}.json")
        if guildJSON['antiraid']['roles']['delete'] == True:
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                if entry.target.id == role.id:
                    if entry.user.id == self.bot.user.id:
                        return 
                    if await check_id_perms(entry.user, entry.user.guild, 2): return
                    try: await entry.user.ban(reason="Antiraid: Role Supprimé")
                    except Exception: pass
                    try:
                        backrole = await role.guild.create_role(
                            name=role.name,
                            permissions=role.permissions,
                            colour=role.colour,
                            display_icon=role.display_icon,
                            mentionable=role.mentionable,
                            reason="Antiraid: Role Recréé car supprimé",
                            hoist=role.hoist
                        )
                        await backrole.edit(
                            position=role.position,
                        )
                    except Exception: return
                    break

async def setup(bot):
    await bot.add_cog(guildRoleDeleteAntiraid(bot))
