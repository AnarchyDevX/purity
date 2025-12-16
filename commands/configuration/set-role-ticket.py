import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class setRoleTicket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="set-role-ticket", description="Définir le rôle à mentionner pour une catégorie de ticket")
    @app_commands.describe(
        category="Le nom exact de la catégorie",
        role="Le rôle à mentionner (laisser vide pour supprimer)"
    )
    async def setRoleTicket(self, interaction: discord.Interaction, category: str, role: discord.Role = None):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        # Vérifier que la structure existe
        if 'tickets' not in guildJSON or 'ticket_categories' not in guildJSON['tickets']:
            return await err_embed(
                interaction,
                title="Aucune catégorie",
                description="Aucune catégorie de ticket n'a été configurée.\n\nUtilisez `/ticket-category-add` pour créer une catégorie."
            )
        
        # Vérifier que la catégorie existe
        if category not in guildJSON['tickets']['ticket_categories']:
            available_categories = list(guildJSON['tickets']['ticket_categories'].keys())
            categories_list = '\n'.join([f"• {cat}" for cat in available_categories]) if available_categories else "*Aucune*"
            
            return await err_embed(
                interaction,
                title="Catégorie inexistante",
                description=f"La catégorie **{category}** n'existe pas.\n\n**Catégories disponibles :**\n{categories_list}\n\nUtilisez `/tickets-config` pour gérer les catégories de tickets."
            )
        
        # Mettre à jour le rôle
        guildJSON['tickets']['ticket_categories'][category]['role_id'] = role.id if role else None
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        if role:
            embed = embedBuilder(
                title="`✅`・Rôle configuré",
                description=f"Le rôle {role.mention} sera maintenant mentionné lors de la création d'un ticket **{category}**.",
                color=embed_color(),
                footer=footer()
            )
        else:
            embed = embedBuilder(
                title="`✅`・Rôle supprimé",
                description=f"Le rôle de la catégorie **{category}** a été supprimé.\n\nAucun rôle ne sera mentionné pour cette catégorie.",
                color=embed_color(),
                footer=footer()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @setRoleTicket.autocomplete('category')
    async def category_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if not guildJSON or 'tickets' not in guildJSON or 'ticket_categories' not in guildJSON['tickets']:
            return []
        
        categories = list(guildJSON['tickets']['ticket_categories'].keys())
        
        # Filtrer selon l'entrée de l'utilisateur
        if current:
            categories = [cat for cat in categories if current.lower() in cat.lower()]
        
        return [
            app_commands.Choice(name=cat, value=cat)
            for cat in categories[:25]  # Discord limite à 25 choix
        ]

async def setup(bot):
    await bot.add_cog(setRoleTicket(bot))

