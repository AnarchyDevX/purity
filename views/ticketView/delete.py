import discord
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder

class deleteButtonTicket(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label="Supprimer le ticket",
            emoji="🗑️"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        # Vérifier que l'utilisateur a les permissions modérateur
        if not await check_id_perms(interaction.user, interaction.guild, 1):
            return await err_embed(
                interaction,
                title="Permission manquante",
                description="Vous devez être modérateur pour supprimer un ticket.",
                followup=True
            )
        
        # Créer un embed de confirmation
        confirm_embed = embedBuilder(
            title="`⚠️`・Confirmation de suppression",
            description=f"Êtes-vous sûr de vouloir supprimer définitivement ce ticket ?\n\nCette action est **irréversible**.",
            color=0xFF0000,  # Rouge pour l'avertissement
            footer=footer()
        )
        
        # Créer la vue avec les boutons de confirmation
        from views.ticketView.deleteConfirm import ConfirmDeleteButton, CancelDeleteButton
        confirm_view = discord.ui.View(timeout=None)
        confirm_view.add_item(ConfirmDeleteButton())
        confirm_view.add_item(CancelDeleteButton())
        
        # Modifier le message pour afficher la confirmation
        try:
            await interaction.message.edit(embed=confirm_embed, view=confirm_view)
            await interaction.followup.send("⚠️ Veuillez confirmer la suppression du ticket.", ephemeral=True)
        except Exception as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Impossible d'afficher la confirmation: {str(e)}",
                followup=True
            )

