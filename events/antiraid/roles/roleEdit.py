import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildRoleUpdateAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        if before.guild.id in getattr(self.bot, "_backup_loading_guilds", set()):
            return
        guildJSON = load_json_file(f"./configs/{before.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        if guildJSON['antiraid']['roles']['edit'] == True:
            if before.position != after.position:
                return
            async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
                if entry.target.id == before.id:
                    if entry.user.id == self.bot.user.id:
                        return
                    if await check_id_perms(entry.user, entry.user.guild, 2): return
                    try:
                        await entry.user.ban(reason="Antiraid: Role Modifié")
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
                    except discord.Forbidden:
                        # Bot n'a pas les permissions
                        return
                    except discord.HTTPException:
                        # Erreur Discord API
                        return
                    except discord.NotFound:
                        # Role déjà supprimé
                        return
                    break

async def setup(bot):
    await bot.add_cog(guildRoleUpdateAntiraid(bot))