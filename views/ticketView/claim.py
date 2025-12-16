import discord
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class claimButtonTicket(Button):
    def __init__(self, custom_id: str = None):
        if custom_id is None:
            custom_id = "ticket_claim"
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Prendre en charge",
            emoji="✋",
            custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        # Vérifier que l'utilisateur a les permissions modérateur ou un rôle de support
        has_mod_perms = await check_id_perms(interaction.user, interaction.guild, 1)
        has_support_role = False
        
        # Rôle de support par défaut (hardcodé)
        SUPPORT_ROLE_ID = 1366762115594977300
        user_roles = [role.id for role in interaction.user.roles]
        has_support_role = SUPPORT_ROLE_ID in user_roles
        
        # Vérifier si l'utilisateur a un des rôles de support configurés dans la config
        if not has_support_role:
            guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
            if guildJSON and 'tickets' in guildJSON and 'roles' in guildJSON['tickets']:
                support_roles = guildJSON['tickets']['roles']
                has_support_role = any(role_id in user_roles for role_id in support_roles)
        
        if not has_mod_perms and not has_support_role:
            return await err_embed(
                interaction,
                title="Permission manquante",
                description="Vous devez être modérateur ou avoir un rôle de support pour prendre en charge un ticket.",
                followup=True
            )
        
        # Charger la configuration pour récupérer la catégorie "pris_en_charge"
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        # Vérifier que la catégorie "pris_en_charge" est configurée
        pris_en_charge_id = guildJSON.get('tickets', {}).get('categories', {}).get('pris_en_charge')
        target_category = None
        if pris_en_charge_id:
            target_category = interaction.guild.get_channel(pris_en_charge_id)
            if not target_category or not isinstance(target_category, discord.CategoryChannel):
                target_category = None
        
        try:
            # Ajouter les permissions pour le modérateur qui a claim le ticket
            overwrite = interaction.channel.overwrites_for(interaction.user)
            overwrite.view_channel = True
            overwrite.send_messages = True
            await interaction.channel.set_permissions(interaction.user, overwrite=overwrite)
            
            # Déplacer le ticket vers la catégorie "pris_en_charge" si configurée
            if target_category:
                await interaction.channel.edit(category=target_category, reason="Ticket pris en charge")
            
            # Envoyer un message visible pour indiquer la prise en charge
            embed = embedBuilder(
                title="`✅`・Ticket pris en charge",
                description=f"Ce ticket a été pris en charge par {interaction.user.mention}",
                color=embed_color(),
                footer=footer()
            )
            
            # Créer les nouveaux boutons (pause et close) avec custom_id basé sur le channel
            view = discord.ui.View(timeout=None)
            from views.ticketView.pause import pauseButtonTicket
            from views.ticketView.close import closeButtonTicket
            view.add_item(pauseButtonTicket(custom_id=f"ticket_pause_{interaction.channel.id}"))
            view.add_item(closeButtonTicket(custom_id=f"ticket_close_{interaction.channel.id}"))
            
            # Envoyer le message dans le channel
            message = await interaction.channel.send(embed=embed, view=view)
            # Ajouter la vue au bot pour la persistance
            self.bot.add_view(view, message_id=message.id)
            
            # Message de confirmation
            if target_category:
                await interaction.followup.send(f"✅ Ticket pris en charge et déplacé dans {target_category.mention} !", ephemeral=True)
            else:
                await interaction.followup.send(f"✅ Ticket pris en charge avec succès !", ephemeral=True)
        except discord.Forbidden:
            await err_embed(
                interaction,
                title="Permission manquante",
                description="Je n'ai pas la permission de modifier ce salon.",
                followup=True
            )
        except discord.HTTPException as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue: {str(e)}",
                followup=True
            )

