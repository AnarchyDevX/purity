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
        if not pris_en_charge_id:
            return await err_embed(
                interaction,
                title="Catégorie non configurée",
                description="La catégorie 'Pris en charge' n'est pas configurée. Utilisez `/ticket-categories-config` pour la configurer.",
                followup=True
            )
        
        target_category = interaction.guild.get_channel(pris_en_charge_id)
        if not target_category or not isinstance(target_category, discord.CategoryChannel):
            return await err_embed(
                interaction,
                title="Catégorie introuvable",
                description="La catégorie 'Pris en charge' configurée n'existe pas.",
                followup=True
            )
        
        # Déplacer le ticket
        try:
            await interaction.channel.edit(category=target_category)
            
            # Ajouter les permissions pour le modérateur qui a claim le ticket
            overwrite = interaction.channel.overwrites_for(interaction.user)
            overwrite.view_channel = True
            overwrite.send_messages = True
            await interaction.channel.set_permissions(interaction.user, overwrite=overwrite)
            
            # Mettre à jour l'embed avec le claim
            embed = embedBuilder(
                title="`✅`・Ticket pris en charge",
                description=f"Ce ticket a été pris en charge par {interaction.user.mention}",
                color=embed_color(),
                footer=footer()
            )
            
            # Trouver le message d'embed initial et le modifier
            async for message in interaction.channel.history(limit=10):
                if message.embeds and len(message.embeds) > 0 and message.embeds[0].title and "Tickets" in message.embeds[0].title:
                    view = discord.ui.View(timeout=None)
                    from views.ticketView.pause import pauseButtonTicket
                    from views.ticketView.close import closeButtonTicket
                    view.add_item(pauseButtonTicket())
                    view.add_item(closeButtonTicket())
                    await message.edit(embed=embed, view=view)
                    break
            
            await interaction.followup.send(f"✅ Ticket pris en charge et déplacé dans {target_category.mention}", ephemeral=True)
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

