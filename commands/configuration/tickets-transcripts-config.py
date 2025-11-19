import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json
from typing import Dict, Any

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
        # Defer immédiatement pour éviter l'expiration de l'interaction
        try:
            await interaction.response.defer(ephemeral=True)
        except discord.InteractionResponded:
            # L'interaction a déjà été répondue
            pass
        except Exception as e:
            print(f"[TICKETS-TRANSCRIPTS-CONFIG] Erreur lors du defer: {e}")
            return
        
        # Vérifier les permissions APRÈS le defer
        config: Dict[str, Any] = load_json()
        guildConfig = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildConfig is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas.",
                followup=True
            )
        
        interactionUser: int = interaction.user.id
        isOwner: bool = interactionUser in guildConfig['ownerlist']
        has_perms = (interactionUser in config['buyer'] or isOwner)
        
        if not has_perms:
            return await err_embed(
                interaction,
                title="Commande non autorisée",
                description="Vous n'avez pas la permission d'utiliser cette commande.",
                followup=True
            )
        
        guildJSON = guildConfig
        
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
                
                # S'assurer que l'ID est bien un entier
                channel_id = int(channel.id)
                guildJSON['tickets']['logs'] = channel_id
                
                # Vérifier que le canal est accessible
                test_channel = interaction.guild.get_channel(channel_id)
                if not test_channel:
                    try:
                        test_channel = await interaction.client.fetch_channel(channel_id)
                    except:
                        return await err_embed(
                            interaction,
                            title="Canal inaccessible",
                            description=f"Le canal {channel.mention} n'est pas accessible. Vérifiez que le bot a accès à ce canal.",
                            followup=True
                        )
                
                embed = embedBuilder(
                    title="`✅`・Canal de logs configuré",
                    description=f"Le canal de logs des transcripts a été défini sur {channel.mention} (ID: {channel_id}).",
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
            import os
            try:
                # S'assurer que le dossier configs existe
                os.makedirs('./configs', exist_ok=True)
                
                with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                    json.dump(guildJSON, f, indent=4, ensure_ascii=False)
                
                await interaction.followup.send(embed=embed, ephemeral=True)
            except PermissionError:
                await err_embed(
                    interaction,
                    title="Erreur de permissions",
                    description=f"Impossible d'écrire dans le fichier de configuration. Vérifiez les permissions du dossier configs.",
                    followup=True
                )
            except OSError as e:
                await err_embed(
                    interaction,
                    title="Erreur système",
                    description=f"Erreur lors de l'écriture du fichier: {str(e)}",
                    followup=True
                )
            
        except Exception as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue lors de la configuration: {str(e)}",
                followup=True
            )

async def setup(bot):
    await bot.add_cog(ticketsTranscriptsConfig(bot))

