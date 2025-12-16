import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.ticketSelectButton import ticketSelectButton
import json
import uuid

class ticketPanelCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket-panel-create", description="Créer un panel de tickets avec vos catégories dynamiques")
    @app_commands.describe(
        channel="Le salon où envoyer le panel",
        title="Titre de l'embed (optionnel)",
        description="Description de l'embed (optionnel)"
    )
    async def ticketPanelCreate(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel,
        title: str = None,
        description: str = None
    ):
        if not await check_perms(interaction, 2):
            return
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        # Vérifier qu'il y a des catégories dynamiques
        if 'tickets' not in guildJSON or 'ticket_categories' not in guildJSON['tickets'] or not guildJSON['tickets']['ticket_categories']:
            return await err_embed(
                interaction,
                title="Aucune catégorie",
                description="Vous devez créer des catégories de tickets avant de créer un panel.\n\nUtilisez `/ticket-category-add` pour créer des catégories.",
                followup=True
            )
        
        # Vérifier que la catégorie des nouveaux tickets existe
        if 'categories' not in guildJSON['tickets'] or not guildJSON['tickets']['categories'].get('nouveaux'):
            return await err_embed(
                interaction,
                title="Catégorie manquante",
                description="Vous devez configurer la catégorie 'nouveaux' avant de créer un panel.\n\nUtilisez `/tickets-config` pour la configurer.",
                followup=True
            )
        
        nouveaux_id = guildJSON['tickets']['categories']['nouveaux']
        nouveaux_category = interaction.guild.get_channel(nouveaux_id)
        
        if not nouveaux_category or not isinstance(nouveaux_category, discord.CategoryChannel):
            return await err_embed(
                interaction,
                title="Catégorie introuvable",
                description="La catégorie 'nouveaux' configurée n'existe plus.\n\nUtilisez `/tickets-config` pour la reconfigurer.",
                followup=True
            )
        
        # Créer les options pour le menu déroulant à partir des catégories dynamiques
        options_list = []
        for cat_name, cat_data in guildJSON['tickets']['ticket_categories'].items():
            emoji = cat_data.get('emoji', '🎫')
            options_list.append({
                'title': cat_name,
                'description': f"Ouvrir un ticket {cat_name}",
                'emojis': emoji
            })
        
        # Créer l'embed
        embed_title = title or "🎫 Système de Tickets"
        embed_description = description or "Sélectionnez une catégorie ci-dessous pour ouvrir un ticket.\n\nUn membre du staff vous répondra dès que possible."
        
        embed = embedBuilder(
            title=embed_title,
            description=embed_description,
            color=embed_color(),
            footer=footer()
        )
        
        # Créer la vue avec le menu déroulant
        custom_id = f"ticket_select_{uuid.uuid4().hex}"
        view = discord.ui.View(timeout=None)
        view.add_item(ticketSelectButton(self.bot, None, nouveaux_category, options_list, custom_id=custom_id))
        
        # Envoyer le panel
        try:
            message = await channel.send(embed=embed, view=view)
            
            # Sauvegarder dans la config
            if 'tickets' not in guildJSON:
                guildJSON['tickets'] = {}
            if 'buttons' not in guildJSON['tickets']:
                guildJSON['tickets']['buttons'] = {}
            
            guildJSON['tickets']['buttons'][str(message.id)] = {
                'channel_id': channel.id,
                'message_id': message.id,
                'category_id': nouveaux_id,
                'options_list': options_list,
                'custom_id': custom_id
            }
            
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4, ensure_ascii=False)
            
            success_embed = embedBuilder(
                title="`✅`・Panel créé",
                description=f"Le panel de tickets a été créé avec succès dans {channel.mention} !\n\n**Catégories disponibles:** {len(options_list)}",
                color=embed_color(),
                footer=footer()
            )
            
            # Lister les catégories
            categories_text = "\n".join([f"• {opt['emojis']} {opt['title']}" for opt in options_list])
            success_embed.add_field(name="📋 Catégories", value=categories_text, inline=False)
            
            await interaction.followup.send(embed=success_embed, ephemeral=True)
            
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Erreur de permissions",
                description=f"Je n'ai pas les permissions pour envoyer un message dans {channel.mention}.",
                followup=True
            )
        except discord.HTTPException as e:
            return await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue lors de la création du panel: {str(e)}",
                followup=True
            )

async def setup(bot):
    await bot.add_cog(ticketPanelCreate(bot))

