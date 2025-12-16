"""
Commande principale pour configurer les tickets via un embed interactif
"""
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Select
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class TicketsConfigMainView(View):
    """Vue principale avec tous les boutons de configuration"""
    
    def __init__(self, bot, user_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.user_id = user_id
    
    @discord.ui.button(label="📁 Catégories", style=discord.ButtonStyle.primary, row=0)
    async def categories_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        # Initialiser si nécessaire
        if 'tickets' not in guildJSON:
            guildJSON['tickets'] = {
                "categories": {
                    "nouveaux": None,
                    "pris_en_charge": None,
                    "en_pause": None,
                    "fermes": None
                }
            }
        
        categories = guildJSON.get('tickets', {}).get('categories', {})
        
        # Créer un select menu pour choisir la catégorie à configurer
        select = CategoriesSelectMenu(self.bot, self.user_id, categories)
        view = View(timeout=300)
        view.add_item(select)
        
        embed = embedBuilder(
            title="`📁`・Configuration des catégories",
            description="Sélectionnez la catégorie que vous souhaitez configurer :",
            color=embed_color(),
            footer=footer()
        )
        
        # Afficher l'état actuel
        category_names = {
            "nouveaux": "🆕 Nouveaux tickets",
            "pris_en_charge": "✋ Pris en charge",
            "en_pause": "⏸️ En pause",
            "fermes": "🔒 Fermés"
        }
        
        for key, name in category_names.items():
            cat_id = categories.get(key)
            if cat_id:
                cat = interaction.guild.get_channel(cat_id)
                status = f"✅ {cat.mention}" if cat else f"❌ Canal supprimé (ID: {cat_id})"
            else:
                status = "❌ Non configuré"
            embed.add_field(name=name, value=status, inline=False)
        
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="👥 Rôles", style=discord.ButtonStyle.primary, row=0)
    async def roles_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        # Utiliser la commande existante (gérer l'import avec tirets dans le nom)
        import importlib.util
        import sys
        
        spec = importlib.util.spec_from_file_location(
            "tickets_roles_config",
            "commands/configuration/tickets-roles-config.py"
        )
        tickets_roles_module = importlib.util.module_from_spec(spec)
        sys.modules["tickets_roles_config"] = tickets_roles_module
        spec.loader.exec_module(tickets_roles_module)
        
        ticketsRolesConfig = tickets_roles_module.ticketsRolesConfig
        cog = ticketsRolesConfig(self.bot)
        await cog.ticketsRolesConfig(interaction)
    
    @discord.ui.button(label="👑 Staff Role", style=discord.ButtonStyle.primary, row=0)
    async def staff_role_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        staff_role_id = guildJSON.get('tickets', {}).get('staff_role')
        
        embed = embedBuilder(
            title="`👑`・Rôle Staff",
            description="Le rôle staff a automatiquement accès à tous les tickets.",
            color=embed_color(),
            footer=footer()
        )
        
        if staff_role_id:
            staff_role = interaction.guild.get_role(staff_role_id)
            if staff_role:
                embed.add_field(
                    name="Rôle actuel",
                    value=f"{staff_role.mention} (`{staff_role.id}`)",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Rôle actuel",
                    value=f"❌ Rôle supprimé (ID: {staff_role_id})",
                    inline=False
                )
        else:
            embed.add_field(
                name="Rôle actuel",
                value="❌ Aucun rôle configuré",
                inline=False
            )
        
        embed.add_field(
            name="ℹ️ Information",
            value="Utilisez `/tickets-config` et cliquez sur le bouton **👑 Staff Role** pour configurer le rôle staff.",
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="📄 Transcripts", style=discord.ButtonStyle.primary, row=1)
    async def transcripts_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        transcripts_enabled = guildJSON.get('tickets', {}).get('transcripts', True)
        logs_channel_id = guildJSON.get('tickets', {}).get('logs')
        
        embed = embedBuilder(
            title="`📄`・Configuration des Transcripts",
            description="Les transcripts sont des sauvegardes des conversations de tickets.",
            color=embed_color(),
            footer=footer()
        )
        
        status = "✅ Activé" if transcripts_enabled else "❌ Désactivé"
        embed.add_field(name="État", value=status, inline=True)
        
        if logs_channel_id:
            logs_channel = interaction.guild.get_channel(logs_channel_id)
            if logs_channel:
                embed.add_field(name="Canal de logs", value=logs_channel.mention, inline=True)
            else:
                embed.add_field(name="Canal de logs", value=f"❌ Canal supprimé (ID: {logs_channel_id})", inline=True)
        else:
            embed.add_field(name="Canal de logs", value="❌ Non configuré", inline=True)
        
        embed.add_field(
            name="ℹ️ Configuration",
            value="Utilisez `/tickets-config` et cliquez sur le bouton **📄 Transcripts** pour configurer les transcripts.",
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="📝 Pré-tickets", style=discord.ButtonStyle.primary, row=1)
    async def preticket_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        preticket_category_id = guildJSON.get('tickets', {}).get('preticket_category')
        
        embed = embedBuilder(
            title="`📝`・Configuration des Pré-tickets",
            description="Les pré-tickets sont des formulaires avant la création du ticket officiel.",
            color=embed_color(),
            footer=footer()
        )
        
        if preticket_category_id:
            preticket_category = interaction.guild.get_channel(preticket_category_id)
            if preticket_category:
                embed.add_field(
                    name="Catégorie actuelle",
                    value=f"✅ {preticket_category.mention}",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Catégorie actuelle",
                    value=f"❌ Catégorie supprimée (ID: {preticket_category_id})",
                    inline=False
                )
        else:
            embed.add_field(
                name="Catégorie actuelle",
                value="❌ Non configurée",
                inline=False
            )
        
        embed.add_field(
            name="ℹ️ Configuration",
            value="Utilisez `/tickets-config` et cliquez sur le bouton **📝 Pré-tickets** pour configurer la catégorie des pré-tickets.",
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="➕ Rôle Add User", style=discord.ButtonStyle.secondary, row=2)
    async def adduser_role_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        adduser_role_id = guildJSON.get('tickets', {}).get('add_user_role')
        
        embed = embedBuilder(
            title="`➕`・Rôle Add User",
            description="Rôle autorisé à utiliser la commande `/add user` dans les tickets.",
            color=embed_color(),
            footer=footer()
        )
        
        if adduser_role_id:
            adduser_role = interaction.guild.get_role(adduser_role_id)
            if adduser_role:
                embed.add_field(
                    name="Rôle actuel",
                    value=f"{adduser_role.mention} (`{adduser_role.id}`)",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Rôle actuel",
                    value=f"❌ Rôle supprimé (ID: {adduser_role_id})",
                    inline=False
                )
        else:
            embed.add_field(
                name="Rôle actuel",
                value="❌ Aucun rôle configuré",
                inline=False
            )
        
        embed.add_field(
            name="ℹ️ Configuration",
            value="Utilisez `/tickets-config` et cliquez sur le bouton **➕ Rôle Add User** pour configurer ce rôle.",
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)


class CategoriesSelectMenu(Select):
    """Menu déroulant pour sélectionner une catégorie à configurer"""
    
    def __init__(self, bot, user_id, current_categories):
        self.bot = bot
        self.user_id = user_id
        self.current_categories = current_categories
        
        options = [
            discord.SelectOption(
                label="Nouveaux tickets",
                description="Catégorie pour les nouveaux tickets",
                value="nouveaux",
                emoji="🆕"
            ),
            discord.SelectOption(
                label="Pris en charge",
                description="Catégorie pour les tickets pris en charge",
                value="pris_en_charge",
                emoji="✋"
            ),
            discord.SelectOption(
                label="En pause",
                description="Catégorie pour les tickets en pause",
                value="en_pause",
                emoji="⏸️"
            ),
            discord.SelectOption(
                label="Fermés",
                description="Catégorie pour les tickets fermés",
                value="fermes",
                emoji="🔒"
            )
        ]
        
        super().__init__(
            placeholder="Sélectionnez une catégorie à configurer...",
            options=options,
            min_values=1,
            max_values=1
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        selected = self.values[0]
        
        # Créer un modal pour entrer l'ID de la catégorie
        modal = CategoryConfigModal(self.bot, self.user_id, selected)
        await interaction.response.send_modal(modal)


class CategoryConfigModal(discord.ui.Modal):
    """Modal pour configurer une catégorie"""
    
    def __init__(self, bot, user_id, category_type):
        self.bot = bot
        self.user_id = user_id
        self.category_type = category_type
        
        category_names = {
            "nouveaux": "Nouveaux tickets",
            "pris_en_charge": "Pris en charge",
            "en_pause": "En pause",
            "fermes": "Fermés"
        }
        
        super().__init__(title=f"Configurer {category_names.get(category_type, category_type)}")
        
        self.category_input = discord.ui.TextInput(
            label="ID de la catégorie Discord",
            placeholder="123456789012345678",
            required=True,
            max_length=20
        )
        self.add_item(self.category_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await unauthorized(interaction)
        
        try:
            category_id = int(self.category_input.value)
        except ValueError:
            return await err_embed(
                interaction,
                title="ID invalide",
                description="L'ID de la catégorie doit être un nombre."
            )
        
        category = interaction.guild.get_channel(category_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            return await err_embed(
                interaction,
                title="Catégorie introuvable",
                description="La catégorie spécifiée n'existe pas ou n'est pas une catégorie."
            )
        
        # Sauvegarder directement
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        if 'tickets' not in guildJSON:
            guildJSON['tickets'] = {}
        if 'categories' not in guildJSON['tickets']:
            guildJSON['tickets']['categories'] = {
                "nouveaux": None,
                "pris_en_charge": None,
                "en_pause": None,
                "fermes": None
            }
        
        guildJSON['tickets']['categories'][self.category_type] = category.id
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        category_names = {
            "nouveaux": "Nouveaux tickets",
            "pris_en_charge": "Pris en charge",
            "en_pause": "En pause",
            "fermes": "Fermés"
        }
        
        embed = embedBuilder(
            title="`✅`・Catégorie configurée",
            description=f"La catégorie **{category_names[self.category_type]}** a été définie sur {category.mention}.",
            color=embed_color(),
            footer=footer()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ticketsConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="tickets-config", description="Configuration principale des tickets via un menu interactif")
    async def ticketsConfig(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        # Créer l'embed principal
        embed = embedBuilder(
            title="`⚙️`・Configuration des Tickets",
            description="Utilisez les boutons ci-dessous pour configurer les différents aspects du système de tickets.",
            color=embed_color(),
            footer=footer()
        )
        
        # Afficher un résumé rapide de la configuration
        tickets_config = guildJSON.get('tickets', {})
        
        # Vérifier les catégories
        categories = tickets_config.get('categories', {})
        categories_configured = sum(1 for v in categories.values() if v is not None)
        embed.add_field(
            name="📁 Catégories",
            value=f"{categories_configured}/4 configurées",
            inline=True
        )
        
        # Vérifier les rôles
        roles = tickets_config.get('roles', [])
        embed.add_field(
            name="👥 Rôles de support",
            value=f"{len(roles)} configuré(s)" if roles else "Aucun",
            inline=True
        )
        
        # Vérifier le staff role
        staff_role = tickets_config.get('staff_role')
        embed.add_field(
            name="👑 Rôle Staff",
            value="✅ Configuré" if staff_role else "❌ Non configuré",
            inline=True
        )
        
        # Vérifier les transcripts
        transcripts = tickets_config.get('transcripts', True)
        logs_channel = tickets_config.get('logs')
        transcript_status = "✅ Activé" if transcripts else "❌ Désactivé"
        if logs_channel:
            transcript_status += " + Canal configuré"
        embed.add_field(
            name="📄 Transcripts",
            value=transcript_status,
            inline=True
        )
        
        # Vérifier les pré-tickets
        preticket_category = tickets_config.get('preticket_category')
        embed.add_field(
            name="📝 Pré-tickets",
            value="✅ Configuré" if preticket_category else "❌ Non configuré",
            inline=True
        )
        
        # Créer la vue avec les boutons
        view = TicketsConfigMainView(self.bot, interaction.user.id)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ticketsConfig(bot))

