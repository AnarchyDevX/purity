import discord
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class pauseButtonTicket(Button):
    def __init__(self, custom_id: str = None):
        if custom_id is None:
            custom_id = "ticket_pause"
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="Mettre en pause",
            emoji="⏸️",
            custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        # Vérifier que l'utilisateur a les permissions modérateur
        if not await check_id_perms(interaction.user, interaction.guild, 1):
            return await err_embed(
                interaction,
                title="Permission manquante",
                description="Vous devez être modérateur pour mettre en pause un ticket.",
                followup=True
            )
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        # Vérifier que la catégorie "en_pause" est configurée
        en_pause_id = guildJSON.get('tickets', {}).get('categories', {}).get('en_pause')
        if not en_pause_id:
            return await err_embed(
                interaction,
                title="Catégorie non configurée",
                description="La catégorie 'En pause' n'est pas configurée. Utilisez `/ticket-categories-config` pour la configurer.",
                followup=True
            )
        
        target_category = interaction.guild.get_channel(en_pause_id)
        if not target_category or not isinstance(target_category, discord.CategoryChannel):
            return await err_embed(
                interaction,
                title="Catégorie introuvable",
                description="La catégorie 'En pause' configurée n'existe pas.",
                followup=True
            )
        
        # Déplacer le ticket
        try:
            await interaction.channel.edit(category=target_category)
            
            # Mettre à jour l'embed avec le statut pause
            embed = embedBuilder(
                title="`⏸️`・Ticket en pause",
                description=f"Ce ticket a été mis en pause par {interaction.user.mention}",
                color=embed_color(),
                footer=footer()
            )
            
            # Trouver le message d'embed initial et le modifier
            async for message in interaction.channel.history(limit=10):
                if message.embeds and len(message.embeds) > 0 and message.embeds[0].title:
                    view = discord.ui.View(timeout=None)
                    from views.ticketView.claim import claimButtonTicket
                    from views.ticketView.close import closeButtonTicket
                    view.add_item(claimButtonTicket(custom_id=f"ticket_claim_{interaction.channel.id}"))
                    view.add_item(closeButtonTicket(custom_id=f"ticket_close_{interaction.channel.id}"))
                    await message.edit(embed=embed, view=view)
                    # Ajouter la vue au bot pour la persistance
                    interaction.client.add_view(view, message_id=message.id)
                    break
            
            await interaction.followup.send(f"⏸️ Ticket mis en pause et déplacé dans {target_category.mention}", ephemeral=True)
        except discord.Forbidden:
            await err_embed(
                interaction,
                title="Permission manquante",
                description="Je n'ai pas la permission de déplacer ce salon.",
                followup=True
            )
        except discord.HTTPException as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue: {str(e)}",
                followup=True
            )

