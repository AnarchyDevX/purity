import discord
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class claimButtonTicket(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Prendre en charge",
            emoji="✋"
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
        
        # Ne pas déplacer le ticket, juste l'indiquer comme pris en charge
        try:
            # Ajouter les permissions pour le modérateur qui a claim le ticket
            overwrite = interaction.channel.overwrites_for(interaction.user)
            overwrite.view_channel = True
            overwrite.send_messages = True
            await interaction.channel.set_permissions(interaction.user, overwrite=overwrite)
            
            # Envoyer un message visible pour indiquer la prise en charge
            embed = embedBuilder(
                title="`✅`・Ticket pris en charge",
                description=f"Ce ticket a été pris en charge par {interaction.user.mention}",
                color=embed_color(),
                footer=footer()
            )
            
            # Créer les nouveaux boutons (pause et close)
            view = discord.ui.View(timeout=None)
            from views.ticketView.pause import pauseButtonTicket
            from views.ticketView.close import closeButtonTicket
            view.add_item(pauseButtonTicket())
            view.add_item(closeButtonTicket())
            
            # Envoyer le message dans le channel
            await interaction.channel.send(embed=embed, view=view)
            
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

