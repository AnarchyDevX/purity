import discord
import html
import aiohttp
import uuid
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

async def generate_ticket_transcript(channel: discord.TextChannel, bot_user: discord.ClientUser) -> str:
    """
    Génère un transcript HTML du ticket avec gestion d'erreurs robuste
    
    Args:
        channel: Le canal du ticket
        bot_user: L'utilisateur du bot
        
    Returns:
        str: Le transcript HTML complet
    """
    try:
        transcript = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Transcript - {html.escape(channel.name)}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #36393f;
            color: #dcddde;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            background: #2f3136;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .message {{
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #5865f2;
            background: #2f3136;
            border-radius: 4px;
        }}
        .author {{
            font-weight: bold;
            color: #5865f2;
            margin-bottom: 5px;
        }}
        .timestamp {{
            color: #72767d;
            font-size: 0.85em;
            margin-left: 10px;
        }}
        .content {{
            margin-top: 5px;
            word-wrap: break-word;
        }}
        .attachment {{
            color: #00aff4;
            margin-top: 5px;
        }}
        .embed {{
            border-left: 4px solid #5865f2;
            padding: 10px;
            margin-top: 5px;
            background: #2f3136;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Transcript du ticket: {html.escape(channel.name)}</h1>
        <p>Créé le: {channel.created_at.strftime('%d/%m/%Y à %H:%M:%S')}</p>
        <p>Fermé le: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
    </div>
"""
        
        message_count = 0
        errors_count = 0
        
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                try:
                    message_count += 1
                    
                    # Auteur
                    author_name = message.author.display_name if hasattr(message.author, 'display_name') else str(message.author)
                    author_color = str(message.author.color) if hasattr(message.author, 'color') and message.author.color.value != 0 else "#5865f2"
                    # Valider que la couleur est un hex valide pour éviter l'injection CSS
                    if not author_color.startswith('#'):
                        author_color = "#5865f2"
                    
                    transcript += f"""
    <div class="message">
        <div class="author" style="color: {html.escape(author_color)};">
            {html.escape(author_name)}
            <span class="timestamp">{message.created_at.strftime('%d/%m/%Y à %H:%M:%S')}</span>
        </div>
"""
                    
                    # Contenu du message
                    if message.content:
                        # Échapper le HTML mais préserver les sauts de ligne
                        content = html.escape(message.content).replace('\n', '<br>')
                        transcript += f"        <div class=\"content\">{content}</div>\n"
                    
                    # Pièces jointes
                    if message.attachments:
                        for attachment in message.attachments:
                            try:
                                # Échapper les URLs et noms de fichiers pour éviter XSS
                                safe_url = html.escape(attachment.url)
                                safe_filename = html.escape(attachment.filename)
                                transcript += f'        <div class="attachment">📎 <a href="{safe_url}" style="color: #00aff4;">{safe_filename}</a></div>\n'
                            except Exception as e:
                                errors_count += 1
                                transcript += f'        <div class="attachment">📎 [Erreur lors de la lecture de la pièce jointe: {html.escape(str(e))}]</div>\n'
                    
                    # Embeds
                    if message.embeds:
                        for embed in message.embeds:
                            try:
                                transcript += '        <div class="embed">\n'
                                if embed.title:
                                    transcript += f'            <strong>{html.escape(embed.title)}</strong><br>\n'
                                if embed.description:
                                    desc = html.escape(embed.description).replace('\n', '<br>')
                                    transcript += f'            <div>{desc}</div>\n'
                                if embed.fields:
                                    for field in embed.fields:
                                        transcript += f'            <div><strong>{html.escape(field.name)}</strong><br>{html.escape(field.value).replace(chr(10), "<br>")}</div>\n'
                                transcript += '        </div>\n'
                            except Exception as e:
                                errors_count += 1
                                transcript += f'        <div class="embed">[Erreur lors de la lecture de l\'embed: {html.escape(str(e))}]</div>\n'
                    
                    transcript += "    </div>\n"
                except discord.Forbidden:
                    # Pas de permission pour lire ce message
                    errors_count += 1
                    continue
                except discord.HTTPException as e:
                    # Erreur HTTP lors de la lecture
                    errors_count += 1
                    continue
                except Exception as e:
                    # Autre erreur inattendue
                    errors_count += 1
                    continue
        except discord.Forbidden:
            # Pas de permission pour lire l'historique
            transcript += '    <div class="message"><div class="content">[ERREUR: Pas de permission pour lire l\'historique du canal]</div></div>\n'
        except discord.HTTPException as e:
            # Erreur HTTP lors de la récupération de l'historique
            transcript += f'    <div class="message"><div class="content">[ERREUR HTTP lors de la récupération de l\'historique: {html.escape(str(e))}]</div></div>\n'
        except Exception as e:
            # Erreur inattendue
            transcript += f'    <div class="message"><div class="content">[ERREUR: {html.escape(str(e))}]</div></div>\n'
        
        transcript += f"""
    <div class="header" style="margin-top: 20px;">
        <p>Total de messages: {message_count}</p>
        {f'<p style="color: #faa61a;">⚠️ {errors_count} message(s) n\'ont pas pu être chargés</p>' if errors_count > 0 else ''}
    </div>
</body>
</html>
"""
        
        return transcript
    except Exception as e:
        # En cas d'erreur critique, retourner un transcript minimal
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Transcript - Erreur</title>
</head>
<body>
    <h1>Erreur lors de la génération du transcript</h1>
    <p>Une erreur est survenue: {html.escape(str(e))}</p>
    <p>Canal: {html.escape(channel.name)}</p>
    <p>Date: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
</body>
</html>"""

async def upload_transcript_to_vps(transcript: str, vps_url: str, channel_name: str) -> Optional[str]:
    """Upload le transcript sur le VPS et retourne l'URL du fichier"""
    
    try:
        # Générer un nom de fichier unique
        transcript_id = str(uuid.uuid4())[:8]
        # Nettoyer le nom du canal pour le nom de fichier (enlever les caractères invalides)
        safe_channel_name = "".join(c for c in channel_name if c.isalnum() or c in ('-', '_', ' ')).strip()[:50]
        filename = f"transcript-{safe_channel_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{transcript_id}.html"
        
        # Préparer les données pour l'upload
        transcript_bytes = transcript.encode('utf-8')
        
        # Si l'URL se termine par /upload, on utilise POST avec multipart/form-data
        # Sinon on essaie d'uploader directement
        parsed_url = urlparse(vps_url)
        
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('file', transcript_bytes, filename=filename, content_type='text/html')
            
            try:
                async with session.post(vps_url, data=data) as response:
                    if response.status == 200:
                        # Si le serveur retourne l'URL dans la réponse
                        try:
                            result = await response.json()
                            if 'url' in result:
                                return result['url']
                            elif 'link' in result:
                                return result['link']
                        except:
                            pass
                        
                        # Si pas de JSON, construire l'URL depuis la base URL
                        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                        if parsed_url.path and parsed_url.path != '/':
                            base_url += parsed_url.path.rstrip('/')
                        return f"{base_url}/{filename}"
                    else:
                        print(f"[TRANSCRIPT] Erreur upload VPS: Status {response.status}")
                        return None
            except Exception as e:
                print(f"[TRANSCRIPT] Erreur lors de l'upload sur le VPS: {e}")
                return None
    
    except Exception as e:
        print(f"[TRANSCRIPT] Erreur lors de la préparation de l'upload: {e}")
        return None

async def generate_ticket_transcript_txt(channel: discord.TextChannel) -> str:
    """
    Génère un transcript en format texte simple avec gestion d'erreurs robuste
    
    Args:
        channel: Le canal du ticket
        
    Returns:
        str: Le transcript en format texte
    """
    try:
        transcript_txt = f"""
{'='*80}
TRANSCRIPT DU TICKET: {channel.name}
{'='*80}
Créé le: {channel.created_at.strftime('%d/%m/%Y à %H:%M:%S')}
Fermé le: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
{'='*80}

"""
        
        message_count = 0
        errors_count = 0
        
        try:
            async for message in channel.history(limit=None, oldest_first=True):
                try:
                    message_count += 1
                    
                    # Auteur
                    author_name = message.author.display_name if hasattr(message.author, 'display_name') else str(message.author)
                    author_discriminator = f"#{message.author.discriminator}" if hasattr(message.author, 'discriminator') and message.author.discriminator != '0' else ""
                    
                    transcript_txt += f"\n[{message.created_at.strftime('%d/%m/%Y %H:%M:%S')}] {author_name}{author_discriminator}\n"
                    transcript_txt += "-" * 80 + "\n"
                    
                    # Contenu du message
                    if message.content:
                        transcript_txt += f"{message.content}\n"
                    
                    # Pièces jointes
                    if message.attachments:
                        for attachment in message.attachments:
                            try:
                                transcript_txt += f"\n📎 Pièce jointe: {attachment.filename} ({attachment.url})\n"
                            except Exception as e:
                                errors_count += 1
                                transcript_txt += f"\n📎 [Erreur pièce jointe: {str(e)}]\n"
                    
                    # Embeds
                    if message.embeds:
                        for embed in message.embeds:
                            try:
                                transcript_txt += "\n[EMBED]\n"
                                if embed.title:
                                    transcript_txt += f"Titre: {embed.title}\n"
                                if embed.description:
                                    transcript_txt += f"Description: {embed.description}\n"
                                if embed.fields:
                                    for field in embed.fields:
                                        transcript_txt += f"{field.name}: {field.value}\n"
                                transcript_txt += "[FIN EMBED]\n"
                            except Exception as e:
                                errors_count += 1
                                transcript_txt += f"\n[EMBED - Erreur: {str(e)}]\n"
                    
                    transcript_txt += "\n"
                except discord.Forbidden:
                    errors_count += 1
                    continue
                except discord.HTTPException:
                    errors_count += 1
                    continue
                except Exception as e:
                    errors_count += 1
                    continue
        except discord.Forbidden:
            transcript_txt += "\n[ERREUR: Pas de permission pour lire l'historique]\n"
        except discord.HTTPException as e:
            transcript_txt += f"\n[ERREUR HTTP: {str(e)}]\n"
        except Exception as e:
            transcript_txt += f"\n[ERREUR: {str(e)}]\n"
        
        transcript_txt += f"\n{'='*80}\n"
        transcript_txt += f"Total de messages: {message_count}\n"
        if errors_count > 0:
            transcript_txt += f"⚠️ {errors_count} message(s) n'ont pas pu être chargés\n"
        transcript_txt += f"{'='*80}\n"
        
        return transcript_txt
    except Exception as e:
        # Fallback minimal en cas d'erreur critique
        return f"""
{'='*80}
TRANSCRIPT DU TICKET: {channel.name}
{'='*80}
ERREUR LORS DE LA GÉNÉRATION
{'='*80}
Erreur: {str(e)}
Canal: {channel.name}
Date: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
{'='*80}
"""

async def send_ticket_transcript(channel: discord.TextChannel, transcript: str, logs_channel: Optional[discord.TextChannel], vps_url: Optional[str] = None, use_txt: bool = True) -> Optional[discord.Message]:
    """
    Envoie le transcript dans le salon de logs avec fallback robuste
    
    Args:
        channel: Le canal du ticket
        transcript: Le transcript HTML (pour fallback)
        logs_channel: Le canal de logs où envoyer
        vps_url: URL du VPS (optionnel, non utilisé si use_txt=True)
        use_txt: Utiliser le format TXT (recommandé)
        
    Returns:
        discord.Message ou None si erreur
    """
    if not logs_channel:
        return None
    
    try:
        # Si on veut utiliser le format TXT (recommandé)
        if use_txt:
            import io
            from discord import File
            
            try:
                # Générer le transcript en TXT
                transcript_txt = await generate_ticket_transcript_txt(channel)
                transcript_bytes = transcript_txt.encode('utf-8')
                
                # Nettoyer le nom du canal pour le nom de fichier
                safe_channel_name = "".join(c for c in channel.name if c.isalnum() or c in ('-', '_', ' ')).strip()[:50]
                transcript_file = File(
                    io.BytesIO(transcript_bytes),
                    filename=f"transcript-{safe_channel_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
                )
                
                # Créer l'embed
                embed = discord.Embed(
                    title="📄 Transcript de ticket",
                    description=f"Transcript du ticket **{channel.name}**",
                    color=0x5865f2,
                    timestamp=datetime.now()
                )
                embed.add_field(name="Ticket", value=channel.mention if channel else channel.name, inline=False)
                embed.add_field(name="Créé le", value=channel.created_at.strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
                embed.add_field(name="Fermé le", value=datetime.now().strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
                
                return await logs_channel.send(embed=embed, file=transcript_file)
            except Exception as e:
                # Fallback: utiliser le transcript HTML si TXT échoue
                print(f"[TRANSCRIPT] Erreur lors de la génération TXT, fallback HTML: {e}")
                return await send_ticket_transcript(channel, transcript, logs_channel, vps_url, use_txt=False)
        
        # Fallback: format HTML (si TXT a échoué)
        import io
        from discord import File
        
        # Nettoyer le nom du canal pour le nom de fichier
        safe_channel_name = "".join(c for c in channel.name if c.isalnum() or c in ('-', '_', ' ')).strip()[:50]
        
        # Essayer d'uploader sur VPS si configuré
        transcript_url = None
        if vps_url:
            try:
                transcript_url = await upload_transcript_to_vps(transcript, vps_url, channel.name)
            except Exception as e:
                print(f"[TRANSCRIPT] Erreur upload VPS: {e}")
        
        # Créer l'embed
        embed = discord.Embed(
            title="📄 Transcript de ticket",
            description=f"Transcript du ticket **{channel.name}**",
            color=0x5865f2,
            timestamp=datetime.now()
        )
        embed.add_field(name="Ticket", value=channel.mention if channel else channel.name, inline=False)
        embed.add_field(name="Créé le", value=channel.created_at.strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
        embed.add_field(name="Fermé le", value=datetime.now().strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
        
        # Si on a une URL VPS, l'ajouter à l'embed
        if transcript_url:
            embed.add_field(name="🔗 Lien du transcript", value=f"[Cliquez ici pour voir le transcript]({transcript_url})", inline=False)
            return await logs_channel.send(embed=embed)
        else:
            # Fallback final: envoyer le fichier HTML directement
            try:
                transcript_bytes = transcript.encode('utf-8')
                transcript_file = File(
                    io.BytesIO(transcript_bytes),
                    filename=f"transcript-{safe_channel_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
                )
                
                if vps_url:
                    embed.add_field(name="⚠️", value="Impossible d'uploader sur le VPS. Le fichier est envoyé en pièce jointe.", inline=False)
                
                return await logs_channel.send(embed=embed, file=transcript_file)
            except Exception as e:
                # Dernier fallback: envoyer juste l'embed avec un message d'erreur
                embed.add_field(name="❌ Erreur", value=f"Impossible d'envoyer le transcript en fichier: {str(e)}", inline=False)
                return await logs_channel.send(embed=embed)
    
    except discord.Forbidden:
        # Pas de permissions pour envoyer dans le canal de logs
        return None
    except discord.HTTPException as e:
        # Erreur HTTP lors de l'envoi
        return None
    except Exception as e:
        # Autre erreur inattendue
        return None

