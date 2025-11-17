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
        if guildJSON is None: return  # Config n'existe pas
        if guildJSON['antiraid']["rank"]["down"] == True:
            # Chercher le rôle retiré (pas ajouté)
            removedRole: Optional[discord.Role] = next((role for role in before.roles if role not in after.roles), None)
            if removedRole:
                # Vérifier si le rôle fait partie de l'autorole (changement automatique)
                autorole_list = guildJSON.get('configuration', {}).get('autorole', [])
                if removedRole.id in autorole_list:
                    return  # Rôle automatique, ignorer
                
                async for entry in before.guild.audit_logs(limit=5, action=discord.AuditLogAction.member_role_update):
                    # Vérification de timing pour éviter les race conditions
                    time_diff = (discord.utils.utcnow() - entry.created_at).total_seconds()
                    if time_diff > 5:  # Ignorer les entries anciennes de plus de 5 secondes
                        continue
                    
                    if entry.target.id == after.id:
                        if entry.user.id == self.bot.user.id:
                            return  # Changement fait par le bot lui-même
                        if entry.user.bot:
                            return  # Changement fait par un bot
                        if await check_id_perms(entry.user, entry.user.guild, 2): return
                        
                        try:
                            await entry.user.ban(reason="Antiraid: Rank Down")
                        except discord.Forbidden:
                            # Bot n'a pas les permissions
                            pass
                        except discord.HTTPException:
                            # Erreur Discord API
                            pass
                        except discord.NotFound:
                            # User déjà banni
                            pass
                        try:
                            await after.add_roles(removedRole)
                        except discord.Forbidden:
                            # Bot n'a pas les permissions
                            return
                        except discord.HTTPException:
                            # Erreur Discord API
                            return
                        break
async def setup(bot):
    await bot.add_cog(roleDownAntiraid(bot))