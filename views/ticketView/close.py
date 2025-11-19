import asyncio
import discord
from discord.ext import commands
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder
from functions.ticketTranscript import generate_ticket_transcript, send_ticket_transcript, generate_ticket_transcript_txt
from datetime import datetime
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
        # Vérifier que la structure tickets existe
        if 'tickets' in guildJSON and guildJSON['tickets'].get('transcripts', False):
            # Initialiser la structure si nécessaire
            if 'logs' not in guildJSON['tickets']:
                guildJSON['tickets']['logs'] = None
            
            logs_channel_id = guildJSON['tickets'].get('logs')
            
            # Debug: logger l'ID récupéré
            print(f"[TRANSCRIPT DEBUG] logs_channel_id récupéré: {logs_channel_id} (type: {type(logs_channel_id)})")
            
            # Convertir en int si c'est une chaîne ou un nombre
            if logs_channel_id is not None:
                try:
                    # Si c'est déjà un int, pas besoin de conversion
                    if isinstance(logs_channel_id, int):
                        pass  # Déjà un int
                    elif isinstance(logs_channel_id, str):
                        logs_channel_id = int(logs_channel_id)
                    else:
                        logs_channel_id = int(logs_channel_id)
                    print(f"[TRANSCRIPT DEBUG] logs_channel_id converti: {logs_channel_id}")
                except (ValueError, TypeError) as e:
                    print(f"[TRANSCRIPT DEBUG] Erreur conversion logs_channel_id: {e}")
                    logs_channel_id = None
            
            if logs_channel_id and logs_channel_id != 0:
                print(f"[TRANSCRIPT DEBUG] Tentative de récupération du canal {logs_channel_id}")
                # Essayer d'abord avec get_channel (cache), puis fetch_channel (API) si échec
                logs_channel = interaction.guild.get_channel(logs_channel_id)
                if not logs_channel:
                    try:
                        logs_channel = await interaction.client.fetch_channel(logs_channel_id)
                        print(f"[TRANSCRIPT DEBUG] Canal récupéré via fetch_channel: {logs_channel}")
                    except discord.NotFound:
                        print(f"[TRANSCRIPT DEBUG] Canal {logs_channel_id} non trouvé (NotFound)")
                        logs_channel = None
                    except discord.Forbidden:
                        print(f"[TRANSCRIPT DEBUG] Pas d'accès au canal {logs_channel_id} (Forbidden)")
                        logs_channel = None
                    except discord.HTTPException as e:
                        print(f"[TRANSCRIPT DEBUG] Erreur HTTP lors de la récupération du canal {logs_channel_id}: {e}")
                        logs_channel = None
                
                if logs_channel:
                    print(f"[TRANSCRIPT DEBUG] Canal trouvé: {logs_channel.name} (type: {type(logs_channel)})")
                else:
                    print(f"[TRANSCRIPT DEBUG] Canal non trouvé pour l'ID {logs_channel_id}")
                
                if logs_channel and isinstance(logs_channel, discord.TextChannel):
                    print(f"[TRANSCRIPT DEBUG] Canal valide, génération du transcript...")
                    transcript_sent = False
                    try:
                        # Vérifier les permissions du bot dans le canal de logs
                        bot_member = logs_channel.guild.get_member(interaction.client.user.id)
                        if not bot_member:
                            bot_member = await logs_channel.guild.fetch_member(interaction.client.user.id)
                        
                        perms = logs_channel.permissions_for(bot_member)
                        if not perms.send_messages or not perms.attach_files or not perms.embed_links:
                            raise discord.Forbidden("Le bot n'a pas les permissions nécessaires dans le canal de logs")
                        
                        # Générer le transcript HTML (nécessaire même si use_txt=True pour le fallback)
                        transcript = await generate_ticket_transcript(channel, interaction.client.user)
                        # Envoyer le transcript (format texte, pas de VPS)
                        result = await send_ticket_transcript(channel, transcript, logs_channel, None, use_txt=True)
                        if result:
                            transcript_sent = True
                            # Confirmer à l'utilisateur que le transcript a été envoyé
                            await interaction.followup.send(
                                embed=embedBuilder(
                                    title="`✅`・Transcript généré",
                                    description=f"Le transcript a été envoyé avec succès dans {logs_channel.mention}.",
                                    color=embed_color(),
                                    footer=footer()
                                ),
                                ephemeral=True
                            )
                    except discord.Forbidden:
                        await logs(f"Erreur de permissions lors de la génération du transcript pour le ticket {channel.id}", 4, interaction)
                        # Essayer le fallback TXT direct
                        try:
                            from functions.ticketTranscript import generate_ticket_transcript_txt
                            import io
                            from discord import File
                            transcript_txt = await generate_ticket_transcript_txt(channel)
                            transcript_file = File(
                                io.BytesIO(transcript_txt.encode('utf-8')),
                                filename=f"transcript-{channel.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
                            )
                            await logs_channel.send(
                                embed=embedBuilder(
                                    title="📄 Transcript de ticket (Fallback)",
                                    description=f"Transcript du ticket **{channel.name}**",
                                    color=embed_color(),
                                    footer=footer()
                                ),
                                file=transcript_file
                            )
                            transcript_sent = True
                        except:
                            pass
                    except discord.HTTPException as e:
                        await logs(f"Erreur HTTP lors de la génération du transcript pour le ticket {channel.id}: {str(e)}", 4, interaction)
                        await interaction.followup.send(
                            embed=embedBuilder(
                                title="`⚠️`・Erreur HTTP",
                                description=f"Une erreur HTTP est survenue lors de la génération du transcript: {str(e)}",
                                color=embed_color(),
                                footer=footer()
                            ),
                            ephemeral=True
                        )
                    except Exception as e:
                        # Si la génération du transcript échoue, continuer quand même avec la fermeture
                        await logs(f"Erreur lors de la génération du transcript pour le ticket {channel.id}: {str(e)}", 4, interaction)
                        # Essayer le fallback TXT minimal
                        try:
                            from functions.ticketTranscript import generate_ticket_transcript_txt
                            import io
                            from discord import File
                            transcript_txt = await generate_ticket_transcript_txt(channel)
                            transcript_file = File(
                                io.BytesIO(transcript_txt.encode('utf-8')),
                                filename=f"transcript-{channel.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
                            )
                            await logs_channel.send(
                                embed=embedBuilder(
                                    title="📄 Transcript de ticket (Fallback)",
                                    description=f"Transcript du ticket **{channel.name}**\n⚠️ Certaines erreurs sont survenues lors de la génération.",
                                    color=0xfaa61a,
                                    footer=footer()
                                ),
                                file=transcript_file
                            )
                            transcript_sent = True
                        except:
                            pass
                    
                    # Notifier l'utilisateur si le transcript n'a pas pu être envoyé
                    if not transcript_sent:
                        await interaction.followup.send(
                            embed=embedBuilder(
                                title="`⚠️`・Transcript non généré",
                                description="Le transcript n'a pas pu être généré ou envoyé. Le ticket sera quand même fermé.\n\n**Vérifiez :**\n- Que le canal de logs existe toujours\n- Que le bot a les permissions d'envoyer des messages dans ce canal\n- Consultez les logs du bot pour plus de détails",
                                color=0xfaa61a,
                                footer=footer()
                            ),
                            ephemeral=True
                        )
                else:
                    # Canal de logs configuré mais introuvable
                    await interaction.followup.send(
                        embed=embedBuilder(
                            title="`⚠️`・Canal de logs introuvable",
                            description=f"Le canal de logs des transcripts (ID: {logs_channel_id}) est configuré mais n'existe plus ou n'est pas accessible.\n\n**Solution :** Utilisez `/tickets-transcripts-config` avec l'action **'Configurer le canal de logs'** et sélectionnez un canal valide.",
                            color=0xfaa61a,
                            footer=footer()
                        ),
                        ephemeral=True
                    )
            else:
                # Canal de logs non configuré - proposer d'envoyer en DM
                try:
                    # Essayer d'envoyer le transcript en DM à l'utilisateur qui ferme le ticket
                    transcript_txt = await generate_ticket_transcript_txt(channel)
                    import io
                    from discord import File
                    transcript_file = File(
                        io.BytesIO(transcript_txt.encode('utf-8')),
                        filename=f"transcript-{channel.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
                    )
                    embed_dm = embedBuilder(
                        title="📄 Transcript de ticket",
                        description=f"Transcript du ticket **{channel.name}**\n\n⚠️ **Note :** Le canal de logs n'est pas configuré sur le serveur. Utilisez `/tickets-transcripts-config` avec l'action **'Configurer le canal de logs'** pour configurer un canal.",
                        color=0xfaa61a,
                        footer=footer()
                    )
                    embed_dm.add_field(name="Ticket", value=f"#{channel.name}", inline=False)
                    embed_dm.add_field(name="Créé le", value=channel.created_at.strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
                    embed_dm.add_field(name="Fermé le", value=datetime.now().strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
                    
                    try:
                        await interaction.user.send(embed=embed_dm, file=transcript_file)
                        await interaction.followup.send(
                            embed=embedBuilder(
                                title="`✅`・Transcript envoyé en MP",
                                description=f"Le transcript a été envoyé dans vos messages privés car aucun canal de logs n'est configuré.\n\n**Pour configurer un canal :** Utilisez `/tickets-transcripts-config` avec l'action **'Configurer le canal de logs'**.",
                                color=embed_color(),
                                footer=footer()
                            ),
                            ephemeral=True
                        )
                    except discord.Forbidden:
                        # L'utilisateur a désactivé les DMs
                        await interaction.followup.send(
                            embed=embedBuilder(
                                title="`⚠️`・Canal de logs non configuré",
                                description=f"Les transcripts sont activés mais aucun canal de logs n'est configuré.\n\n**Solution :** Utilisez `/tickets-transcripts-config` avec l'action **'Configurer le canal de logs'** et sélectionnez un canal où envoyer les transcripts.\n\n*Note : Impossible d'envoyer le transcript en MP (messages privés désactivés).*",
                                color=0xfaa61a,
                                footer=footer()
                            ),
                            ephemeral=True
                        )
                except Exception as e:
                    # Erreur lors de la génération du transcript
                    await interaction.followup.send(
                        embed=embedBuilder(
                            title="`⚠️`・Canal de logs non configuré",
                            description=f"Les transcripts sont activés mais aucun canal de logs n'est configuré.\n\n**Solution :** Utilisez `/tickets-transcripts-config` avec l'action **'Configurer le canal de logs'** et sélectionnez un canal où envoyer les transcripts.\n\n*Erreur lors de la génération du transcript : {str(e)}*",
                            color=0xfaa61a,
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