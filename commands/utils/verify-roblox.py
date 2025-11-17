import discord
import json
import aiohttp
import time
import asyncio
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from web_server import get_verification_queue

class robloxVerify(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.verification_codes = {}  # Stocke les codes: {code: {roblox_username, timestamp, guild_id}}
        self._verification_task = None
    
    async def cog_load(self):
        """Démarrer la tâche de monitoring de la queue de vérification"""
        self._verification_task = asyncio.create_task(self._monitor_verification_queue())
    
    async def cog_unload(self):
        """Arrêter la tâche de monitoring"""
        if self._verification_task:
            self._verification_task.cancel()
    
    async def _monitor_verification_queue(self):
        """Monitorer la queue de vérification du serveur web"""
        queue_obj = get_verification_queue()
        while True:
            try:
                # Vérifier toutes les 0.5 secondes s'il y a des codes en attente
                await asyncio.sleep(0.5)
                
                # Traiter tous les codes disponibles dans la queue
                while not queue_obj.empty():
                    try:
                        verification_data = queue_obj.get_nowait()
                        code = verification_data['code'].upper()
                        username = verification_data['username']
                        
                        # Enregistrer le code
                        self.verification_codes[code] = {
                            'roblox_username': username,
                            'timestamp': verification_data['timestamp'],
                            'guild_id': None  # Sera déterminé lors de la vérification Discord
                        }
                        
                        print(f"[VERIFICATION] Code créé via web: {code} pour {username}")
                    except Exception as e:
                        print(f"[VERIFICATION] Erreur lors du traitement: {e}")
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[VERIFICATION] Erreur dans le monitoring: {e}")
                await asyncio.sleep(1)

    @app_commands.command(name="verify", description="Vérifier votre compte Roblox")
    async def verify(self, interaction: discord.Interaction, roblox_username: str, code: str):
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration de ce serveur n'existe pas.",
                followup=True
            )
        
        if not guildJSON['roblox_verification']['active']:
            return await err_embed(
                interaction,
                title="Vérification désactivée",
                description="La vérification Roblox n'est pas activée sur ce serveur.",
                followup=True
            )
        
        role_id = guildJSON['roblox_verification']['role']
        if role_id is None:
            return await err_embed(
                interaction,
                title="Rôle manquant",
                description="Aucun rôle de vérification n'est configuré.",
                followup=True
            )
        
        role = discord.utils.get(interaction.guild.roles, id=role_id)
        if role is None:
            return await err_embed(
                interaction,
                title="Rôle introuvable",
                description="Le rôle de vérification configuré n'existe pas.",
                followup=True
            )
        
        # Vérifier si l'utilisateur a déjà le rôle
        if role in interaction.user.roles:
            return await err_embed(
                interaction,
                title="Déjà vérifié",
                description=f"Vous avez déjà le rôle {role.mention}.",
                followup=True
            )
        
        # Vérifier si le code existe
        code_upper = code.upper()
        if code_upper not in self.verification_codes:
            return await err_embed(
                interaction,
                title="Code invalide",
                description=f"Le code `{code}` n'existe pas ou a expiré.",
                followup=True
            )
        
        verification_data = self.verification_codes[code_upper]
        
        # Vérifier si le code n'a pas expiré (10 minutes)
        if time.time() - verification_data['timestamp'] > 600:
            del self.verification_codes[code_upper]
            return await err_embed(
                interaction,
                title="Code expiré",
                description="Le code de vérification a expiré. Veuillez rejoindre le jeu Roblox pour obtenir un nouveau code.",
                followup=True
            )
        
        # Vérifier si l'utilisateur Roblox correspond
        if verification_data['roblox_username'].lower() != roblox_username.lower():
            return await err_embed(
                interaction,
                title="Utilisateur incorrect",
                description=f"Ce code appartient à **{verification_data['roblox_username']}**, pas à **{roblox_username}**.",
                followup=True
            )
        
        # Accorder le rôle
        try:
            await interaction.user.add_roles(role)
            success_embed = embedBuilder(
                title="`✅`・Vérification réussie",
                description=f"*Vous avez été vérifié avec succès ! Le rôle {role.mention} vous a été attribué.*",
                color=embed_color(),
                footer=footer()
            )
            await interaction.followup.send(embed=success_embed, ephemeral=True)
            
            # Supprimer le code utilisé
            del self.verification_codes[code_upper]
        except discord.Forbidden:
            await err_embed(
                interaction,
                title="Permission manquante",
                description="Je n'ai pas la permission d'attribuer des rôles.",
                followup=True
            )
        except discord.HTTPException:
            await err_embed(
                interaction,
                title="Erreur Discord",
                description="Une erreur est survenue lors de l'attribution du rôle.",
                followup=True
            )


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Vérifier si le message vient d'un webhook
        if not message.webhook_id:
            return
        
        # Vérifier que le message contient un code de vérification
        # Format attendu: "VERIFY:CODE:USERNAME"
        if message.content and message.content.startswith("VERIFY:"):
            try:
                parts = message.content.split(":")
                if len(parts) != 3:
                    return
                
                _, code, roblox_username = parts
                code_upper = code.upper()
                
                # Créer le code de vérification
                self.verification_codes[code_upper] = {
                    'roblox_username': roblox_username,
                    'timestamp': time.time(),
                    'guild_id': message.guild.id if message.guild else None
                }
                
                print(f"[VERIFICATION] Code créé: {code_upper} pour {roblox_username}")
            except Exception as e:
                print(f"[VERIFICATION] Erreur lors du traitement du webhook: {e}")

    @app_commands.command(name="set-verification-webhook", description="Configurer le webhook de vérification")
    async def set_verification_webhook(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not await check_perms(interaction, 2):
            return
        
        try:
            # Créer le webhook
            webhook = await channel.create_webhook(name="Roblox Verification")
            
            embed = embedBuilder(
                title="`✅`・Webhook créé",
                description=f"Webhook de vérification créé avec succès !\n\n**URL:** `{webhook.url}`\n\nUtilisez cette URL dans votre script Roblox pour envoyer les codes de vérification.",
                color=embed_color(),
                footer=footer()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            await err_embed(
                interaction,
                title="Permission manquante",
                description="Je n'ai pas la permission de créer des webhooks."
            )
        except Exception as e:
            await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue: {str(e)}"
            )


async def setup(bot):
    await bot.add_cog(robloxVerify(bot))
