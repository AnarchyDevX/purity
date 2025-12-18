import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.roleAdd import ticketRoleAddButton
from views.ticketView.roleRemove import ticketRoleRemoveButton


async def open_tickets_roles_config(bot: commands.Bot, interaction: discord.Interaction, user_id: int) -> None:
    """
    Ouvre le panel de configuration des rôles de tickets.
    Réutilisé par la commande /tickets-roles-config et par le bouton du /ticket-config.
    """
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
    view.add_item(ticketRoleAddButton(user_id, bot))
    view.add_item(ticketRoleRemoveButton(user_id, bot))
    await interaction.response.send_message(embed=embed, view=view)


class ticketsRolesConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="tickets-roles-config", description="Configurer les rôles de support pour les tickets")
    async def ticketsRolesConfig(self, interaction: discord.Interaction):
        await open_tickets_roles_config(self.bot, interaction, interaction.user.id)


async def setup(bot):
    await bot.add_cog(ticketsRolesConfig(bot))

