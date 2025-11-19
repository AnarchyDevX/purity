import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.roleAdd import ticketRoleAddButton
from views.ticketView.roleRemove import ticketRoleRemoveButton

class ticketsRolesConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="tickets-roles-config", description="Configurer les rôles de support pour les tickets")
    async def ticketsRolesConfig(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        # Initialiser la structure si nécessaire
        if 'tickets' not in guildJSON:
            guildJSON['tickets'] = {
                "logs": None,
                "transcripts": True,
                "roles": [],
                "claim": True,
                "buttons": {},
                "categories": {
                    "nouveaux": None,
                    "pris_en_charge": None,
                    "en_pause": None,
                    "fermes": None
                }
            }
        
        if 'roles' not in guildJSON['tickets']:
            guildJSON['tickets']['roles'] = []
        
        rolesList = [f"<@&{roleId}> `{roleId}`" for roleId in guildJSON['tickets']['roles']]
        embed = embedBuilder(
            title="`🎫`・Liste des rôles de support",
            description='\n'.join(rolesList) if rolesList else "*Aucun rôle configuré*",
            footer=footer(),
            color=embed_color()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(ticketRoleAddButton(interaction.user.id, self.bot))
        view.add_item(ticketRoleRemoveButton(interaction.user.id, self.bot))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ticketsRolesConfig(bot))

