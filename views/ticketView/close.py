import asyncio
import discord
from discord.ext import commands
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder
from functions.ticketTranscript import generate_ticket_transcript, send_ticket_transcript
import json


class closeButtonTicket(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Fermer",
            emoji="🔒"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Erreur de configuration",
                description="La configuration du serveur n'a pas été trouvée.",
                followup=True
            )
        
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            return await err_embed(
                interaction,
                title="Erreur",
                description="Cette commande ne peut être utilisée que dans un salon de texte.",
                followup=True
            )
        
        # Générer et envoyer le transcript si activé
        if guildJSON['tickets']['transcripts']:
            logs_channel_id = guildJSON['tickets']['logs']
            
            if logs_channel_id:
                logs_channel = interaction.guild.get_channel(logs_channel_id)
                if logs_channel:
                    try:
                        # Générer le transcript HTML (nécessaire même si use_txt=True pour le fallback)
                        transcript = await generate_ticket_transcript(channel, interaction.client.user)
                        # Envoyer le transcript (format texte, pas de VPS)
                        await send_ticket_transcript(channel, transcript, logs_channel, None, use_txt=True)
                    except discord.Forbidden:
                        await logs(f"Erreur de permissions lors de la génération du transcript pour le ticket {channel.id}", 4, interaction)
                    except discord.HTTPException as e:
                        await logs(f"Erreur HTTP lors de la génération du transcript pour le ticket {channel.id}: {str(e)}", 4, interaction)
                    except Exception as e:
                        # Si la génération du transcript échoue, continuer quand même avec la fermeture
                        await logs(f"Erreur lors de la génération du transcript pour le ticket {channel.id}: {str(e)}", 4, interaction)
                else:
                    # Canal de logs configuré mais introuvable
                    await interaction.followup.send(
                        embed=embedBuilder(
                            title="`⚠️`・Canal de logs introuvable",
                            description=f"Le canal de logs des transcripts est configuré mais n'existe plus. Utilisez `/tickets-transcripts-config` pour le reconfigurer.",
                            color=embed_color(),
                            footer=footer()
                        ),
                        ephemeral=True
                    )
            else:
                # Canal de logs non configuré
                await interaction.followup.send(
                    embed=embedBuilder(
                        title="`⚠️`・Canal de logs non configuré",
                        description=f"Les transcripts sont activés mais aucun canal de logs n'est configuré. Utilisez `/tickets-transcripts-config` avec l'action 'Configurer le canal de logs' pour configurer un canal.",
                        color=embed_color(),
                        footer=footer()
                    ),
                    ephemeral=True
                )
        
        # Déplacer vers la catégorie "fermes" ou supprimer
        category_fermes_id = guildJSON['tickets']['categories'].get('fermes')
        if category_fermes_id:
            category_fermes = interaction.guild.get_channel(category_fermes_id)
            if category_fermes and isinstance(category_fermes, discord.CategoryChannel):
                try:
                    await channel.edit(category=category_fermes, reason="Ticket fermé")
                    await interaction.followup.send(
                        embed=embedBuilder(
                            title="`✅`・Ticket fermé",
                            description=f"Le ticket a été déplacé vers la catégorie fermée.",
                            color=embed_color(),
                            footer=footer()
                        ),
                        ephemeral=True
                    )
                    await asyncio.sleep(5)
                    try:
                        await channel.delete(reason="Ticket fermé et transcript généré")
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
                    except discord.HTTPException:
                        pass
                except discord.Forbidden:
                    await err_embed(
                        interaction,
                        title="Erreur de permissions",
                        description="Je n'ai pas les permissions nécessaires pour déplacer ce salon.",
                        followup=True
                    )
                except discord.HTTPException:
                    await err_embed(
                        interaction,
                        title="Erreur",
                        description="Une erreur est survenue lors du déplacement du salon.",
                        followup=True
                    )
            else:
                # Si la catégorie n'existe pas, supprimer directement
                await interaction.followup.send(
                    embed=embedBuilder(
                        title="`✅`・Ticket fermé",
                        description=f"Le ticket va être supprimé dans 5 secondes.",
                        color=embed_color(),
                        footer=footer()
                    ),
                    ephemeral=True
                )
                await asyncio.sleep(5)
                try:
                    await channel.delete(reason="Ticket fermé et transcript généré")
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    pass
                except discord.HTTPException:
                    pass
        else:
            # Pas de catégorie "fermes" configurée, supprimer directement
            await interaction.followup.send(
                embed=embedBuilder(
                    title="`✅`・Ticket fermé",
                    description=f"Le ticket va être supprimé dans 5 secondes.",
                    color=embed_color(),
                    footer=footer()
                ),
                ephemeral=True
            )
            await asyncio.sleep(5)
            try:
                await channel.delete(reason="Ticket fermé et transcript généré")
            except discord.Forbidden:
                pass
            except discord.NotFound:
                pass
            except discord.HTTPException:
                pass