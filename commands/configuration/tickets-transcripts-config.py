import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class ticketsTranscriptsConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="tickets-transcripts-config", description="Configurer le système de transcription des tickets")
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Activer les transcripts", value="enable"),
            app_commands.Choice(name="Désactiver les transcripts", value="disable"),
            app_commands.Choice(name="Configurer le canal de logs", value="channel")
        ]
    )
    async def ticketsTranscriptsConfig(self, interaction: discord.Interaction, action: str, 
                                      channel: discord.TextChannel | None = None):
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
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            if action == "enable":
                guildJSON['tickets']['transcripts'] = True
                embed = embedBuilder(
                    title="`✅`・Transcripts activés",
                    description="Le système de transcription des tickets est maintenant activé.",
                    color=embed_color(),
                    footer=footer()
                )
            
            elif action == "disable":
                guildJSON['tickets']['transcripts'] = False
                embed = embedBuilder(
                    title="`❌`・Transcripts désactivés",
                    description="Le système de transcription des tickets est maintenant désactivé.",
                    color=embed_color(),
                    footer=footer()
                )
            
            elif action == "channel":
                if not channel:
                    return await err_embed(
                        interaction,
                        title="Canal manquant",
                        description="Veuillez spécifier un canal de logs pour les transcripts.",
                        followup=True
                    )
                
                guildJSON['tickets']['logs'] = channel.id
                embed = embedBuilder(
                    title="`✅`・Canal de logs configuré",
                    description=f"Le canal de logs des transcripts a été défini sur {channel.mention}.",
                    color=embed_color(),
                    footer=footer()
                )
            else:
                # Action invalide (ne devrait jamais arriver avec les choices)
                return await err_embed(
                    interaction,
                    title="Action invalide",
                    description=f"L'action '{action}' n'est pas valide.",
                    followup=True
                )
            
            # Sauvegarder seulement si une action valide a été effectuée
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4, ensure_ascii=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue lors de la configuration: {str(e)}",
                followup=True
            )

async def setup(bot):
    await bot.add_cog(ticketsTranscriptsConfig(bot))

