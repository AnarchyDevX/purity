import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class ticketsCategoriesConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket-categories-config", description="Configurer les catégories de tickets")
    @app_commands.choices(
        category_type=[
            app_commands.Choice(name="Nouveaux tickets", value="nouveaux"),
            app_commands.Choice(name="Pris en charge", value="pris_en_charge"),
            app_commands.Choice(name="En pause", value="en_pause"),
            app_commands.Choice(name="Fermés", value="fermes")
        ]
    )
    async def ticketCategoriesConfig(self, interaction: discord.Interaction, category_type: str, category: discord.CategoryChannel):
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
                }
            }
        
        if 'categories' not in guildJSON['tickets']:
            guildJSON['tickets']['categories'] = {
                "nouveaux": None,
                "pris_en_charge": None,
                "en_pause": None,
                "fermes": None
            }
        
        # Mapper les noms pour l'affichage
        category_names = {
            "nouveaux": "Nouveaux tickets",
            "pris_en_charge": "Pris en charge",
            "en_pause": "En pause",
            "fermes": "Fermés"
        }
        
        # Sauvegarder la catégorie
        guildJSON['tickets']['categories'][category_type] = category.id
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        embed = embedBuilder(
            title="`✅`・Catégorie configurée",
            description=f"La catégorie **{category_names[category_type]}** a été définie sur {category.mention}.",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ticketsCategoriesConfig(bot))

