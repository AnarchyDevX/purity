import json
import os
import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from models.configuration import configuration

class createConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create-config", description="Créer la configuration du serveur (si elle n'existe pas)")
    async def createConfig(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 3):
            return
        
        config_path = f"./configs/{interaction.guild.id}.json"
        
        # Vérifier si la config existe déjà
        if os.path.exists(config_path):
            return await err_embed(
                interaction,
                title="Configuration existante",
                description="La configuration de ce serveur existe déjà."
            )
        
        # Créer le dossier configs s'il n'existe pas
        os.makedirs("./configs", exist_ok=True)
        
        # Créer la configuration
        try:
            # Ajouter le propriétaire du serveur à l'ownerlist automatiquement
            config_copy = configuration.copy()
            guild_owner_id = interaction.guild.owner.id if interaction.guild.owner else None
            if guild_owner_id and guild_owner_id not in config_copy['ownerlist']:
                config_copy['ownerlist'].append(guild_owner_id)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_copy, f, indent=4, ensure_ascii=False)
            
            embed = embedBuilder(
                title="`✅`・Configuration créée",
                description=f"*La configuration du serveur **{interaction.guild.name}** a été créée avec succès.*\n\n**Note :** Le propriétaire du serveur a été automatiquement ajouté à l'ownerlist.",
                color=embed_color(),
                footer=footer()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            return await err_embed(
                interaction,
                title="Erreur",
                description=f"Impossible de créer la configuration: {str(e)}"
            )

async def setup(bot):
    await bot.add_cog(createConfig(bot))

