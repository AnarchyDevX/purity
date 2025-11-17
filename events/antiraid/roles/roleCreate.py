from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildRoleCreateAntiraid(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        if role.guild.id in getattr(self.bot, "_backup_loading_guilds", set()):
            return
        guildJSON = load_json_file(f"./configs/{role.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        if guildJSON['antiraid']['roles']['create'] == True:
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                if entry.target.id == role.id:
                    if entry.user.id == self.bot.user.id:
                        return 
                    if await check_id_perms(entry.user, entry.user.guild, 2): return
                    try:
                        await entry.user.ban(reason="Antiraid: Role Créé")
                        await role.delete(reason="Antiraid: Role Créé")
                    except discord.Forbidden:
                        # Bot n'a pas les permissions
                        return
                    except discord.HTTPException:
                        # Erreur Discord API
                        return
                    except discord.NotFound:
                        # Role ou user déjà supprimé
                        return
                    break

async def setup(bot):
    await bot.add_cog(guildRoleCreateAntiraid(bot))
