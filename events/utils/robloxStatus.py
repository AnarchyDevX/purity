import discord
import aiohttp
from discord.ext import commands, tasks
from functions.functions import *

class robloxStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.place_id = 88744853552411  # ID du jeu French Donations
        # DÉSACTIVÉ - Utilisez rotatingStatus.py à la place
        # self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(minutes=2)  # Mise à jour toutes les 2 minutes
    async def update_status(self):
        await self.bot.wait_until_ready()
        try:
            # Récupérer le nombre de joueurs depuis l'API Roblox
            async with aiohttp.ClientSession() as session:
                # Utiliser l'API Roblox pour obtenir les infos du jeu
                url = f"https://games.roblox.com/v1/games?placeIds={self.place_id}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('data') and len(data['data']) > 0:
                            game_data = data['data'][0]
                            playing = game_data.get('playing', 0)
                            
                            # Mettre à jour le statut du bot
                            activity = discord.Activity(
                                type=discord.ActivityType.watching,
                                name=f"{playing} joueurs sur French Donations"
                            )
                            await self.bot.change_presence(activity=activity)
                        else:
                            # Si pas de données, utiliser une valeur par défaut
                            activity = discord.Activity(
                                type=discord.ActivityType.watching,
                                name="French Donations"
                            )
                            await self.bot.change_presence(activity=activity)
                    else:
                        # En cas d'erreur API, ne pas changer le statut
                        pass
        except Exception as e:
            # En cas d'erreur, ne pas changer le statut
            print(f"[ROBLOX STATUS] Erreur lors de la mise à jour: {e}")
            pass

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(robloxStatus(bot))

