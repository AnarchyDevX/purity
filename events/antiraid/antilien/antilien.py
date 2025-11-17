import re
import discord
from discord.ext import commands
from functions.functions import *
from datetime import timedelta

class antilienAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Détecte http://, https://, www., et invitations Discord (tous formats)
        # Patterns: http://, https://, www., discord.gg/, discord.com/invite/, discord.io/, etc.
        self.linkRegex = r"(https?://[^\s<>]+|www\.[^\s<>]+|discord\.gg/[^\s<>]+|discord\.io/[^\s<>]+|discord\.com/invite/[^\s<>]+|discord\.com/channels/[^\s<>]+)"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message): return
        if message.author.id == self.bot.user.id: return
        
        guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        
        # Vérifier si l'antilien est activé
        if not guildJSON.get('antiraid', {}).get('antilien', False):
            return
        
        # Vérifier si l'utilisateur est exempté (seulement owner et whitelist, pas les buyers)
        memberId = message.author.id
        isOwner = memberId in guildJSON.get('ownerlist', [])
        isWhitelist = memberId in guildJSON.get('whitelist', [])
        if isOwner or isWhitelist:
            return  # Utilisateur exempté (owner/whitelist uniquement)
        
        # L'antilien est activé et l'utilisateur n'est pas exempté
        # Exception pour Tenor (GIFs)
        if "tenor.com" in message.content.lower():
            return
        
        # Vérifier si le message contient un lien
        if bool(re.search(self.linkRegex, message.content, re.IGNORECASE)):
            # Sauvegarder le contenu avant suppression
            message_content = message.content[:2000] if len(message.content) > 2000 else message.content
            message_author = message.author
            message_channel = message.channel
            message_id = message.id
            message_created_at = message.created_at
            message_author_created_at = message.author.created_at
            message_author_joined_at = message.author.joined_at
            
            # Supprimer le message EN PREMIER (avant tout log)
            try: 
                await message.delete()
            except discord.Forbidden:
                # Bot n'a pas les permissions pour supprimer
                print(f"[ANTILIEN] Erreur: Pas de permissions pour supprimer le message {message_id}")
            except discord.NotFound:
                # Message déjà supprimé, continuer
                pass
            except discord.HTTPException as e:
                # Erreur Discord API
                print(f"[ANTILIEN] Erreur HTTP: {e} pour le message {message_id}")
            except Exception as e:
                # Autre erreur inattendue
                print(f"[ANTILIEN] Erreur inattendue: {e} pour le message {message_id}")
            
            # Envoyer un log dans le canal de logs raid
            logsChannel = await check_if_logs(message.guild, 'raidlogs')
            if logsChannel:
                try:
                    embed: embedBuilder = embedBuilder(
                        description=f"```[{time_now()}] - Raid | Message Contenant Un Lien (Supprimé)```",
                        color=embed_color(),
                        footer=footer(),
                        fields={
                            "`👤`・Membre": (
                                f"{message_author.mention} (`{message_author.id}`) | Créé: `{format_date('year', message_author_created_at)}` | Rejoint: `{format_date('year', message_author_joined_at)}`",
                                False
                            ),
                            "`📝`・Message": (
                                f"Salon: {message_channel.mention} | ID: `{message_id}` | `{format_date('all', message_created_at)}`\n**Contenu:** {message_content[:1000] + '...' if len(message_content) > 1000 else message_content}",
                                False
                            )
                        }
                    )
                    await logsChannel.send(embed=embed)
                except Exception:
                    # Erreur lors de l'envoi du log, continuer quand même
                    pass
            
            # Timeout l'utilisateur
            try: 
                await message_author.timeout(discord.utils.utcnow() + timedelta(minutes=1))
            except discord.Forbidden:
                # Bot n'a pas les permissions
                pass
            except discord.HTTPException:
                # Erreur Discord API
                pass
            
async def setup(bot):
    await bot.add_cog(antilienAntiraid(bot))