import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class ticketsPreticketCategoryConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket-preticket-category-config", description="Définir où les pré-tickets seront créés")
    @app_commands.describe(category="La catégorie où les pré-tickets temporaires seront créés")
    async def ticketPreticketCategoryConfig(self, interaction: discord.Interaction, category: discord.CategoryChannel = None):
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
                "preticket_category": None
            }
        
        # Sauvegarder la catégorie (ou None pour réinitialiser)
        guildJSON['tickets']['preticket_category'] = category.id if category else None
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        if category:
            embed = embedBuilder(
                title="`✅`・Catégorie configurée",
                description=f"Les pré-tickets temporaires seront créés dans {category.mention}.\n\n**Info :** Avant de créer un ticket officiel, le bot créera un channel temporaire dans cette catégorie pour poser les questions de pré-formulaire.",
                color=embed_color(),
                footer=footer()
            )
        else:
            embed = embedBuilder(
                title="`✅`・Catégorie réinitialisée",
                description="La catégorie des pré-tickets a été réinitialisée.\n\n**Attention :** Sans catégorie configurée, le système de pré-formulaire ne fonctionnera pas correctement.",
                color=0xfaa61a,
                footer=footer()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ticketsPreticketCategoryConfig(bot))

