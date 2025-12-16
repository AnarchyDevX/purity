"""
Commande pour synchroniser manuellement les commandes slash avec Discord
Utile pour supprimer les commandes obsolètes du cache Discord
"""
import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class syncCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="sync-commands", description="Synchroniser les commandes slash avec Discord (owner uniquement)")
    async def syncCommands(self, interaction: discord.Interaction):
        """Synchronise les commandes slash avec Discord pour mettre à jour la liste des commandes disponibles"""
        # Vérifier les permissions (niveau 3 = owner uniquement)
        if not await check_perms(interaction, 3):
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Sync global (peut prendre du temps)
            await interaction.followup.send(
                embed=embedBuilder(
                    title="`⏳`・Synchronisation en cours",
                    description="Synchronisation des commandes globales... Cela peut prendre quelques instants.",
                    color=0xfaa61a,
                    footer=footer()
                ),
                ephemeral=True
            )
            
            synced_global = await self.bot.tree.sync()
            
            # Sync par serveur (instantané)
            synced_guilds = 0
            failed_guilds = []
            
            for guild in self.bot.guilds:
                try:
                    synced = await self.bot.tree.sync(guild=guild)
                    synced_guilds += 1
                except Exception as e:
                    failed_guilds.append(f"{guild.name}: {str(e)}")
            
            # Message de succès
            description = f"✅ **Synchronisation terminée !**\n\n"
            description += f"**Commandes globales synchronisées :** {len(synced_global)}\n"
            description += f"**Serveurs synchronisés :** {synced_guilds}/{len(self.bot.guilds)}\n"
            
            if failed_guilds:
                description += f"\n⚠️ **Erreurs :** {len(failed_guilds)} serveur(s) n'ont pas pu être synchronisés."
            
            description += "\n\n**Note :** Les commandes supprimées peuvent prendre jusqu'à 1 heure pour disparaître du cache Discord global, mais elles sont immédiatement supprimées sur les serveurs synchronisés."
            
            embed = embedBuilder(
                title="`✅`・Synchronisation réussie",
                description=description,
                color=embed_color(),
                footer=footer()
            )
            
            if failed_guilds and len(failed_guilds) <= 5:
                # Afficher les erreurs si peu nombreuses
                error_text = "\n".join(failed_guilds[:5])
                embed.add_field(
                    name="⚠️ Erreurs",
                    value=f"```{error_text}```",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            await err_embed(
                interaction,
                title="Erreur de synchronisation",
                description=f"Une erreur est survenue lors de la synchronisation : {str(e)}",
                followup=True
            )

async def setup(bot):
    await bot.add_cog(syncCommands(bot))

