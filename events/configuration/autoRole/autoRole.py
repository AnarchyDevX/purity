import discord
import os
import json
from discord.ext import commands
from functions.functions import *

class autoRole(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            guildJSON = load_json_file(f'./configs/{member.guild.id}.json')
            if not guildJSON:
                # Config n'existe pas, on ne peut rien faire
                return
            
            roleList: list[int] = guildJSON.get('configuration', {}).get('autorole', [])
            depractatedRoles: list[int] = []
            
            for roles in roleList:
                role: discord.Role | None = discord.utils.get(member.guild.roles, id=roles)
                if role:
                    try:
                        await member.add_roles(role)
                    except discord.Forbidden:
                        # Bot n'a pas les permissions
                        pass
                    except discord.HTTPException:
                        # Erreur Discord API
                        pass
                else:
                    depractatedRoles.append(roles)
            
            # Si des rôles obsolètes ont été trouvés, mettre à jour la config
            if depractatedRoles:
                # Créer une copie pour éviter de modifier la liste pendant l'itération
                for role in depractatedRoles[:]:
                    roleList.remove(role)
                
                # S'assurer que le dossier configs existe
                os.makedirs('./configs', exist_ok=True)
                
                # Sauvegarder la config avec gestion d'erreurs
                try:
                    with open(f'./configs/{member.guild.id}.json', 'w', encoding='utf-8') as f:
                        json.dump(guildJSON, f, indent=4, ensure_ascii=False)
                except PermissionError:
                    # Erreur de permissions, logger mais ne pas crasher
                    print(f"[AUTOROLE] Permission denied: Impossible d'écrire dans ./configs/{member.guild.id}.json")
                except OSError as e:
                    # Autre erreur système
                    print(f"[AUTOROLE] Erreur OS lors de l'écriture de la config: {e}")
                except Exception as e:
                    # Erreur inattendue
                    print(f"[AUTOROLE] Erreur inattendue lors de l'écriture de la config: {e}")
        except Exception as e:
            # Erreur globale, ne pas crasher le bot
            print(f"[AUTOROLE] Erreur dans on_member_join pour {member.guild.id}: {e}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoRole(bot))