"""
Système de vérification automatique des permissions pour les tickets
Vérifie que le rôle staff a bien accès à tous les tickets ouverts
"""
import discord
from discord.ext import commands, tasks
from functions.functions import *
import json

class ticketPermissionChecker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.check_permissions.start()

    def cog_unload(self):
        self.check_permissions.cancel()

    @tasks.loop(minutes=5)  # Vérifier toutes les 5 minutes
    async def check_permissions(self):
        """
        Vérifie automatiquement que tous les tickets ont les bonnes permissions
        pour le rôle staff configuré
        """
        await self.bot.wait_until_ready()
        
        for guild in self.bot.guilds:
            try:
                # Charger la configuration du serveur
                guildJSON = load_json_file(f"./configs/{guild.id}.json")
                if not guildJSON:
                    continue
                
                # Vérifier si un staff_role est configuré
                staff_role_id = guildJSON.get('tickets', {}).get('staff_role')
                if not staff_role_id:
                    continue
                
                staff_role = guild.get_role(staff_role_id)
                if not staff_role:
                    # Le rôle n'existe plus, logger l'erreur
                    print(f"[TICKET CHECK] Rôle staff {staff_role_id} introuvable sur {guild.name}")
                    continue
                
                # Récupérer toutes les catégories de tickets
                ticket_categories = []
                if 'tickets' in guildJSON and 'categories' in guildJSON['tickets']:
                    categories = guildJSON['tickets']['categories']
                    for cat_id in [categories.get('nouveaux'), categories.get('pris_en_charge'), 
                                  categories.get('en_pause'), categories.get('fermes')]:
                        if cat_id:
                            cat = guild.get_channel(cat_id)
                            if cat and isinstance(cat, discord.CategoryChannel):
                                ticket_categories.append(cat)
                
                # Vérifier tous les channels dans ces catégories
                fixed_count = 0
                for category in ticket_categories:
                    for channel in category.channels:
                        if isinstance(channel, discord.TextChannel):
                            # Vérifier si le rôle staff a accès
                            overwrite = channel.overwrites_for(staff_role)
                            
                            # Si le rôle n'a pas view_channel ou si les permissions sont incomplètes
                            if not overwrite.view_channel or not overwrite.send_messages:
                                try:
                                    # Corriger les permissions
                                    await channel.set_permissions(
                                        staff_role,
                                        view_channel=True,
                                        send_messages=True,
                                        read_message_history=True,
                                        attach_files=True,
                                        embed_links=True,
                                        reason="Correction automatique des permissions staff"
                                    )
                                    fixed_count += 1
                                    print(f"[TICKET CHECK] Permissions corrigées pour {channel.name} sur {guild.name}")
                                except discord.Forbidden:
                                    print(f"[TICKET CHECK] Pas de permission pour corriger {channel.name} sur {guild.name}")
                                except discord.HTTPException as e:
                                    print(f"[TICKET CHECK] Erreur HTTP lors de la correction de {channel.name}: {e}")
                                except Exception as e:
                                    print(f"[TICKET CHECK] Erreur lors de la correction de {channel.name}: {e}")
                
                if fixed_count > 0:
                    print(f"[TICKET CHECK] {fixed_count} ticket(s) corrigé(s) sur {guild.name}")
                    
            except Exception as e:
                print(f"[TICKET CHECK] Erreur lors de la vérification pour {guild.name}: {e}")
                continue

    @check_permissions.before_loop
    async def before_check_permissions(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(ticketPermissionChecker(bot))

