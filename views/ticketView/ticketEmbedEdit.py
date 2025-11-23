import discord
from discord.ui import Button, View, Modal, TextInput, Select
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class TicketEmbedEditView(View):
    def __init__(self, user_id, bot):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.bot = bot
    
    @discord.ui.button(label="Modifier le titre", style=discord.ButtonStyle.primary, emoji="✏️", row=0)
    async def edit_title(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        modal = TitleEditModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if modal.new_title:
            await self._update_template(interaction, 'title', modal.new_title)
    
    @discord.ui.button(label="Modifier la description", style=discord.ButtonStyle.primary, emoji="📝", row=0)
    async def edit_description(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        modal = DescriptionEditModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if modal.new_description:
            await self._update_template(interaction, 'description', modal.new_description)
    
    @discord.ui.button(label="Modifier la couleur", style=discord.ButtonStyle.primary, emoji="🎨", row=0)
    async def edit_color(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        modal = ColorEditModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if modal.new_color:
            await self._update_template(interaction, 'color', modal.new_color)
    
    @discord.ui.button(label="Modifier le footer", style=discord.ButtonStyle.primary, emoji="📌", row=1)
    async def edit_footer(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        modal = FooterEditModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if modal.new_footer is not None:  # Peut être vide pour réinitialiser
            await self._update_template(interaction, 'footer', modal.new_footer if modal.new_footer else None)
    
    @discord.ui.button(label="Affichage des champs", style=discord.ButtonStyle.secondary, emoji="👁️", row=1)
    async def toggle_fields(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if not guildJSON:
            return await err_embed(interaction, title="Erreur", description="Configuration introuvable.")
        
        template = guildJSON['tickets']['embed_template']
        
        # Créer un select menu pour choisir les champs à afficher
        options = [
            discord.SelectOption(
                label="Utilisateur",
                value="show_user",
                description="Afficher le champ 'Utilisateur'",
                emoji="👤",
                default=template.get('show_user', True)
            ),
            discord.SelectOption(
                label="Pseudo Roblox",
                value="show_roblox",
                description="Afficher le champ 'Pseudo Roblox'",
                emoji="🎮",
                default=template.get('show_roblox', True)
            ),
            discord.SelectOption(
                label="Catégorie",
                value="show_category",
                description="Afficher le champ 'Catégorie'",
                emoji="📁",
                default=template.get('show_category', True)
            ),
            discord.SelectOption(
                label="Raison",
                value="show_reason",
                description="Afficher le champ 'Raison'",
                emoji="📝",
                default=template.get('show_reason', True)
            )
        ]
        
        select = FieldToggleSelect(options, self.user_id, self.bot)
        view = View(timeout=60)
        view.add_item(select)
        
        await interaction.response.send_message(
            embed=embedBuilder(
                title="`👁️`・Affichage des champs",
                description="Sélectionnez les champs que vous souhaitez afficher dans l'embed des tickets.",
                color=embed_color(),
                footer=footer()
            ),
            view=view,
            ephemeral=True
        )
    
    @discord.ui.button(label="Réinitialiser", style=discord.ButtonStyle.danger, emoji="🔄", row=2)
    async def reset_template(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if not guildJSON:
            return await err_embed(interaction, title="Erreur", description="Configuration introuvable.", ephemeral=True)
        
        # Réinitialiser le template
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
        
        # Mettre à jour l'aperçu
        from commands.configuration.ticket_embed_config import ticketEmbedConfig
        cog = ticketEmbedConfig(self.bot)
        preview = cog._create_preview_embed(guildJSON['tickets']['embed_template'], interaction.user)
        
        await interaction.response.edit_message(
            embeds=[
                embedBuilder(
                    title="`✅`・Template réinitialisé",
                    description="Le template de l'embed des tickets a été réinitialisé aux valeurs par défaut.",
                    color=embed_color(),
                    footer=footer()
                ),
                preview
            ],
            view=self
        )
    
    @discord.ui.button(label="Terminer", style=discord.ButtonStyle.success, emoji="✅", row=2)
    async def finish(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        await interaction.response.edit_message(
            embed=embedBuilder(
                title="`✅`・Configuration terminée",
                description="Le template de l'embed des tickets a été sauvegardé avec succès !\n\nIl sera utilisé pour tous les nouveaux tickets créés.",
                color=embed_color(),
                footer=footer()
            ),
            view=None
        )
        self.stop()
    
    async def _update_template(self, interaction: discord.Interaction, key: str, value):
        """Met à jour le template et rafraîchit l'aperçu"""
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if not guildJSON:
            return
        
        guildJSON['tickets']['embed_template'][key] = value
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        # Mettre à jour l'aperçu
        from commands.configuration.ticket_embed_config import ticketEmbedConfig
        cog = ticketEmbedConfig(self.bot)
        preview = cog._create_preview_embed(guildJSON['tickets']['embed_template'], interaction.user)
        
        # Récupérer le message original
        try:
            original_message = await interaction.original_response()
            await original_message.edit(embeds=[original_message.embeds[0], preview])
        except:
            pass


class TitleEditModal(Modal):
    def __init__(self):
        super().__init__(title="Modifier le titre de l'embed", timeout=300)
        self.new_title = None
        
        self.title_input = TextInput(
            label="Titre",
            placeholder="Ex: 🎫 Ticket - {category}",
            max_length=256,
            required=True
        )
        self.add_item(self.title_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        self.new_title = self.title_input.value
        await interaction.response.defer()


class DescriptionEditModal(Modal):
    def __init__(self):
        super().__init__(title="Modifier la description", timeout=300)
        self.new_description = None
        
        self.description_input = TextInput(
            label="Description",
            placeholder="Ex: Bienvenue {user}, un staff va vous aider.",
            style=discord.TextStyle.paragraph,
            max_length=4000,
            required=True
        )
        self.add_item(self.description_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        self.new_description = self.description_input.value
        await interaction.response.defer()


class ColorEditModal(Modal):
    def __init__(self):
        super().__init__(title="Modifier la couleur", timeout=300)
        self.new_color = None
        
        self.color_input = TextInput(
            label="Couleur (format hexadécimal)",
            placeholder="Ex: #FF5733 ou FF5733 (laisser vide pour défaut)",
            max_length=7,
            required=False
        )
        self.add_item(self.color_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        color = self.color_input.value.strip()
        if color:
            # Retirer le # si présent
            color = color.replace('#', '')
            # Valider le format hexadécimal
            try:
                int(color, 16)
                self.new_color = color
            except ValueError:
                await interaction.response.send_message(
                    embed=embedBuilder(
                        title="`❌`・Couleur invalide",
                        description="Le format de couleur est invalide. Utilisez le format hexadécimal (ex: FF5733).",
                        color=0xff0000,
                        footer=footer()
                    ),
                    ephemeral=True
                )
                return
        else:
            self.new_color = None
        
        await interaction.response.defer()


class FooterEditModal(Modal):
    def __init__(self):
        super().__init__(title="Modifier le footer", timeout=300)
        self.new_footer = None
        
        self.footer_input = TextInput(
            label="Texte du footer",
            placeholder="Laisser vide pour utiliser le footer par défaut",
            max_length=2048,
            required=False
        )
        self.add_item(self.footer_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        self.new_footer = self.footer_input.value.strip() if self.footer_input.value else None
        await interaction.response.defer()


class FieldToggleSelect(Select):
    def __init__(self, options, user_id, bot):
        super().__init__(
            placeholder="Sélectionnez les champs à afficher...",
            min_values=0,
            max_values=len(options),
            options=options
        )
        self.user_id = user_id
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if not guildJSON:
            return await err_embed(interaction, title="Erreur", description="Configuration introuvable.")
        
        # Mettre à jour les champs
        selected_values = self.values
        guildJSON['tickets']['embed_template']['show_user'] = 'show_user' in selected_values
        guildJSON['tickets']['embed_template']['show_roblox'] = 'show_roblox' in selected_values
        guildJSON['tickets']['embed_template']['show_category'] = 'show_category' in selected_values
        guildJSON['tickets']['embed_template']['show_reason'] = 'show_reason' in selected_values
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        await interaction.response.send_message(
            embed=embedBuilder(
                title="`✅`・Champs mis à jour",
                description="L'affichage des champs a été mis à jour avec succès !",
                color=embed_color(),
                footer=footer()
            ),
            ephemeral=True
        )

