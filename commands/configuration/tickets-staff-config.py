"""
Commande pour configurer le rôle staff des tickets
Ce rôle aura automatiquement accès à tous les tickets créés
"""
import discord
import json
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class ticketsStaffConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setstaffrole", description="Définir le rôle staff qui aura automatiquement accès à tous les tickets")
    async def setStaffRole(self, interaction: discord.Interaction, role: discord.Role):
        """
        Définit le rôle staff pour les tickets
        
        Args:
            interaction: L'interaction Discord
            role: Le rôle à définir comme staff role
        """
        # Vérifier les permissions (niveau 2 = owner ou buyer)
        if not await check_perms(interaction, 2):
            return
        
        # Charger la configuration du serveur
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas. Utilisez `/create-config` pour la créer."
            )
        
        # Initialiser la structure tickets si nécessaire
        if 'tickets' not in guildJSON:
            guildJSON['tickets'] = {
                "logs": None,
                "transcripts": True,
                "roles": [],
                "staff_role": None,
                "claim": True,
                "buttons": {},
                "categories": {
                    "nouveaux": None,
                    "pris_en_charge": None,
                    "en_pause": None,
                    "fermes": None
                }
            }
        
        # Vérifier que le rôle existe et est valide
        if not role:
            return await err_embed(
                interaction,
                title="Rôle invalide",
                description="Le rôle spécifié n'existe pas."
            )
        
        # Vérifier que le bot peut gérer ce rôle (position)
        if role.position >= interaction.guild.me.top_role.position:
            return await err_embed(
                interaction,
                title="Rôle trop élevé",
                description=f"Le rôle {role.mention} est plus élevé que mon rôle le plus haut. Je ne peux pas lui donner des permissions."
            )
        
        # Sauvegarder le rôle staff
        guildJSON['tickets']['staff_role'] = role.id
        
        # Sauvegarder la configuration
        try:
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        except Exception as e:
            return await err_embed(
                interaction,
                title="Erreur de sauvegarde",
                description=f"Impossible de sauvegarder la configuration: {str(e)}"
            )
        
        # Message de confirmation
        embed = embedBuilder(
            title="`✅`・Rôle staff configuré",
            description=f"Le rôle {role.mention} a été défini comme rôle staff.\n\n**Ce rôle aura automatiquement accès à tous les tickets créés.**",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Logger l'action
        await logs(f"Rôle staff défini: {role.name} ({role.id})", 1, interaction)

async def setup(bot):
    await bot.add_cog(ticketsStaffConfig(bot))

