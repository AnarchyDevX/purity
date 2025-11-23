import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.ticketEmbedEdit import TicketEmbedEditView
import json

class ticketEmbedConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket-embed-config", description="Personnaliser l'embed des tickets")
    async def ticketEmbedConfig(self, interaction: discord.Interaction):
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
                },
                "embed_template": {
                    "title": "🎫 Ticket - {category}",
                    "description": "Un membre du staff va vous prendre en charge, merci de patienter.",
                    "color": None,
                    "footer": None,
                    "show_roblox": True,
                    "show_reason": True,
                    "show_category": True,
                    "show_user": True
                }
            }
        
        if 'embed_template' not in guildJSON['tickets']:
            guildJSON['tickets']['embed_template'] = {
                "title": "🎫 Ticket - {category}",
                "description": "Un membre du staff va vous prendre en charge, merci de patienter.",
                "color": None,
                "footer": None,
                "show_roblox": True,
                "show_reason": True,
                "show_category": True,
                "show_user": True
            }
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        template = guildJSON['tickets']['embed_template']
        
        # Créer un aperçu de l'embed
        preview_embed = self._create_preview_embed(template, interaction.user)
        
        # Créer la vue d'édition
        view = TicketEmbedEditView(interaction.user.id, self.bot)
        
        info_embed = embedBuilder(
            title="`🎨`・Configuration de l'embed des tickets",
            description="Utilisez les boutons ci-dessous pour personnaliser l'embed qui apparaîtra dans les tickets.\n\n**Variables disponibles :**\n`{category}` - Nom de la catégorie\n`{user}` - Mention de l'utilisateur\n`{username}` - Nom de l'utilisateur\n`{roblox}` - Pseudo Roblox\n`{reason}` - Raison du ticket",
            color=embed_color(),
            footer=footer()
        )
        
        await interaction.response.send_message(
            embeds=[info_embed, preview_embed],
            view=view,
            ephemeral=True
        )
    
    def _create_preview_embed(self, template, user):
        """Crée un aperçu de l'embed avec des valeurs d'exemple"""
        title = template.get('title', '🎫 Ticket - {category}').replace('{category}', 'Support').replace('{user}', user.mention).replace('{username}', user.name)
        description = template.get('description', 'Un membre du staff va vous prendre en charge, merci de patienter.')
        
        # Remplacer les variables dans la description
        description = description.replace('{user}', user.mention).replace('{username}', user.name).replace('{category}', 'Support')
        
        color_value = template.get('color')
        if color_value:
            try:
                color = int(color_value, 16) if isinstance(color_value, str) else color_value
            except:
                color = embed_color()
        else:
            color = embed_color()
        
        preview = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        
        # Ajouter les champs selon la configuration
        if template.get('show_user', True):
            preview.add_field(name="👤 Utilisateur", value=user.mention, inline=True)
        
        if template.get('show_roblox', True):
            preview.add_field(name="🎮 Pseudo Roblox", value="`ExempleRoblox`", inline=True)
        
        if template.get('show_category', True):
            preview.add_field(name="📁 Catégorie", value="Support", inline=True)
        
        if template.get('show_reason', True):
            preview.add_field(name="📝 Raison", value="Ceci est un exemple de raison pour le ticket.", inline=False)
        
        footer_text = template.get('footer')
        if footer_text:
            preview.set_footer(text=footer_text)
        else:
            preview.set_footer(text=footer())
        
        return preview

async def setup(bot):
    await bot.add_cog(ticketEmbedConfig(bot))

