import discord
from discord.ext import commands
from functions.functions import *

class presenceUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after):
        guildJSON = load_json_file(f'./configs/{before.guild.id}.json')
        if guildJSON is None:
            return  # Config n'existe pas pour ce serveur
        if guildJSON.get('soutien') is None:
            return  # Configuration soutien n'existe pas
        content = guildJSON['soutien']['needed']
        role = before.guild.get_role(guildJSON['soutien']['role'])
        if guildJSON['soutien']['active'] == True:
            try:
                if content in str(after.activity) and role not in after.roles:
                    if role in before.roles:
                        return
                    else:
                        role = discord.utils.get(before.guild.roles, id=guildJSON['soutien']['role'])
                        await before.add_roles(role)
                if content in str(before.activity) and content in str(after.activity):
                    return
                if content in str(before.activity) and content not in str(after.activity):
                    role = discord.utils.get(before.guild.roles, id=guildJSON['soutien']['role'])
                    await after.remove_roles(role)
            except discord.Forbidden:
                # Bot n'a pas les permissions pour ajouter/retirer les rôles
                return
            except discord.HTTPException:
                # Erreur Discord API
                return
            except discord.NotFound:
                # Rôle ou membre introuvable
                return

async def setup(bot):
    await bot.add_cog(presenceUpdate(bot))