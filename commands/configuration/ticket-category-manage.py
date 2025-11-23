import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class ticketCategoryManage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket-category-add", description="Ajouter une catégorie de ticket dynamique")
    @app_commands.describe(
        name="Le nom de la catégorie (ex: Support, Report Discord, Report In-Game)",
        emoji="L'emoji pour cette catégorie (optionnel)",
        role="Le rôle à mentionner pour cette catégorie (optionnel)",
        category="La catégorie Discord où créer les tickets (optionnel, sera créée auto si non fournie)"
    )
    async def ticketCategoryAdd(
        self, 
        interaction: discord.Interaction, 
        name: str,
        emoji: str = None,
        role: discord.Role = None,
        category: discord.CategoryChannel = None
    ):
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
                "ticket_categories": {}
            }
        
        if 'ticket_categories' not in guildJSON['tickets']:
            guildJSON['tickets']['ticket_categories'] = {}
        
        # Vérifier si la catégorie existe déjà
        if name in guildJSON['tickets']['ticket_categories']:
            return await err_embed(
                interaction,
                title="Catégorie existante",
                description=f"La catégorie **{name}** existe déjà.\n\nUtilisez `/ticket-category-remove` pour la supprimer d'abord."
            )
        
        # Si aucune catégorie Discord n'est fournie, en créer une automatiquement
        if category is None:
            try:
                await interaction.response.defer(ephemeral=True)
                category = await interaction.guild.create_category(
                    name=f"🎫 {name}",
                    reason=f"Catégorie de ticket créée automatiquement pour {name}"
                )
            except discord.Forbidden:
                return await err_embed(
                    interaction,
                    title="Erreur de permissions",
                    description="Je n'ai pas les permissions pour créer une catégorie.\n\nVeuillez fournir une catégorie existante ou me donner les permissions nécessaires.",
                    followup=True
                )
            except discord.HTTPException as e:
                return await err_embed(
                    interaction,
                    title="Erreur",
                    description=f"Impossible de créer la catégorie: {str(e)}\n\nVeuillez fournir une catégorie existante.",
                    followup=True
                )
        
        # Sauvegarder la catégorie
        guildJSON['tickets']['ticket_categories'][name] = {
            "role_id": role.id if role else None,
            "discord_category_id": category.id,
            "emoji": emoji
        }
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        embed = embedBuilder(
            title="`✅`・Catégorie ajoutée",
            description=f"La catégorie **{name}** a été créée avec succès !",
            color=embed_color(),
            footer=footer()
        )
        embed.add_field(name="📁 Catégorie Discord", value=category.mention, inline=False)
        if emoji:
            embed.add_field(name="😀 Emoji", value=emoji, inline=True)
        if role:
            embed.add_field(name="👥 Rôle", value=role.mention, inline=True)
        
        embed.add_field(
            name="ℹ️ Information",
            value="Cette catégorie apparaîtra automatiquement dans le menu de création de tickets.",
            inline=False
        )
        
        if category.id == category.id and not role:
            embed.add_field(
                name="⚠️ Conseil",
                value=f"Utilisez `/set-role-ticket {name} @role` pour définir le rôle à mentionner pour cette catégorie.",
                inline=False
            )
        
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket-category-remove", description="Supprimer une catégorie de ticket dynamique")
    @app_commands.describe(
        name="Le nom de la catégorie à supprimer",
        delete_category="Supprimer aussi la catégorie Discord (par défaut: non)"
    )
    async def ticketCategoryRemove(
        self, 
        interaction: discord.Interaction, 
        name: str,
        delete_category: bool = False
    ):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        # Vérifier que la catégorie existe
        if 'tickets' not in guildJSON or 'ticket_categories' not in guildJSON['tickets']:
            return await err_embed(
                interaction,
                title="Aucune catégorie",
                description="Aucune catégorie de ticket n'a été configurée."
            )
        
        if name not in guildJSON['tickets']['ticket_categories']:
            return await err_embed(
                interaction,
                title="Catégorie inexistante",
                description=f"La catégorie **{name}** n'existe pas.\n\nUtilisez `/ticket-category-list` pour voir les catégories disponibles."
            )
        
        # Récupérer les infos avant de supprimer
        category_data = guildJSON['tickets']['ticket_categories'][name]
        category_id = category_data.get('discord_category_id')
        
        # Supprimer la catégorie de la config
        del guildJSON['tickets']['ticket_categories'][name]
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        # Supprimer la catégorie Discord si demandé
        if delete_category and category_id:
            await interaction.response.defer(ephemeral=True)
            category_channel = interaction.guild.get_channel(category_id)
            if category_channel and isinstance(category_channel, discord.CategoryChannel):
                try:
                    await category_channel.delete(reason=f"Catégorie de ticket {name} supprimée")
                    embed = embedBuilder(
                        title="`✅`・Catégorie supprimée",
                        description=f"La catégorie **{name}** et sa catégorie Discord ont été supprimées.",
                        color=embed_color(),
                        footer=footer()
                    )
                except discord.Forbidden:
                    embed = embedBuilder(
                        title="`⚠️`・Catégorie partiellement supprimée",
                        description=f"La catégorie **{name}** a été supprimée de la configuration, mais je n'ai pas pu supprimer la catégorie Discord (permissions insuffisantes).",
                        color=0xfaa61a,
                        footer=footer()
                    )
                except discord.HTTPException:
                    embed = embedBuilder(
                        title="`⚠️`・Catégorie partiellement supprimée",
                        description=f"La catégorie **{name}** a été supprimée de la configuration, mais une erreur est survenue lors de la suppression de la catégorie Discord.",
                        color=0xfaa61a,
                        footer=footer()
                    )
            else:
                embed = embedBuilder(
                    title="`✅`・Catégorie supprimée",
                    description=f"La catégorie **{name}** a été supprimée. La catégorie Discord n'a pas été trouvée.",
                    color=embed_color(),
                    footer=footer()
                )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = embedBuilder(
                title="`✅`・Catégorie supprimée",
                description=f"La catégorie **{name}** a été supprimée de la configuration.",
                color=embed_color(),
                footer=footer()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket-category-list", description="Lister toutes les catégories de tickets dynamiques")
    async def ticketCategoryList(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        # Vérifier s'il y a des catégories
        if 'tickets' not in guildJSON or 'ticket_categories' not in guildJSON['tickets'] or not guildJSON['tickets']['ticket_categories']:
            return await err_embed(
                interaction,
                title="Aucune catégorie",
                description="Aucune catégorie de ticket n'a été configurée.\n\nUtilisez `/ticket-category-add` pour en créer une."
            )
        
        embed = embedBuilder(
            title="`📋`・Catégories de tickets",
            description="Voici toutes les catégories de tickets configurées :",
            color=embed_color(),
            footer=footer()
        )
        
        for cat_name, cat_data in guildJSON['tickets']['ticket_categories'].items():
            emoji = cat_data.get('emoji', '📁')
            category_id = cat_data.get('discord_category_id')
            role_id = cat_data.get('role_id')
            
            category_mention = f"<#{category_id}>" if category_id else "*Non configurée*"
            role_mention = f"<@&{role_id}>" if role_id else "*Aucun*"
            
            embed.add_field(
                name=f"{emoji} {cat_name}",
                value=f"**Catégorie:** {category_mention}\n**Rôle:** {role_mention}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ticketCategoryManage(bot))

