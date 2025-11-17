import asyncio
import discord
from discord.ui import Button, View
from functions.functions import *

class ConfirmDeleteButton(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label="Oui, supprimer",
            emoji="✅"
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
        
        await interaction.followup.send("🗑️ Le ticket sera supprimé dans 3 secondes...", ephemeral=True)
        await asyncio.sleep(3)
        
        try:
            await interaction.channel.delete()
        except discord.Forbidden:
            await err_embed(
                interaction,
                title="Permission manquante",
                description="Je n'ai pas la permission de supprimer ce salon.",
                followup=True
            )
        except discord.NotFound:
            # Le channel a déjà été supprimé
            pass
        except Exception as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue: {str(e)}",
                followup=True
            )

class CancelDeleteButton(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="Non, annuler",
            emoji="❌"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("❌ Suppression annulée.", ephemeral=True)
        
        # Modifier le message pour retirer les boutons de confirmation
        try:
            embed = interaction.message.embeds[0]
            view = discord.ui.View(timeout=None)
            from views.ticketView.delete import deleteButtonTicket
            view.add_item(deleteButtonTicket())
            await interaction.message.edit(embed=embed, view=view)
        except Exception as e:
            print(f"[DELETE CONFIRM] Erreur lors de la modification du message: {e}")

