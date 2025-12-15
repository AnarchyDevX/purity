import discord
from discord.ext import commands, tasks
from core._colors import Colors
import time
from datetime import datetime

class RotatingStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.C: Colors = Colors()
        self.status_index = 0
        self.start_time = time.time()
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    def format_number(self, num: int) -> str:
        """Formate un nombre avec des séparateurs (ex: 1000 -> 1,000)"""
        return f"{num:,}".replace(",", " ")

    def get_uptime(self) -> str:
        """Calcule et formate l'uptime du bot"""
        uptime_seconds = int(time.time() - self.start_time)
        
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        
        if days > 0:
            return f"{days}j {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def get_total_members(self) -> int:
        """Calcule le nombre total de membres (sans doublons)"""
        unique_members = set()
        for guild in self.bot.guilds:
            for member in guild.members:
                unique_members.add(member.id)
        return len(unique_members)

    def get_total_channels(self) -> int:
        """Calcule le nombre total de channels"""
        total = 0
        for guild in self.bot.guilds:
            total += len(guild.channels)
        return total

    def get_total_bots(self) -> int:
        """Calcule le nombre total de bots (sans doublons)"""
        unique_bots = set()
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.bot:
                    unique_bots.add(member.id)
        return len(unique_bots)

    def get_total_commands(self) -> int:
        """Retourne le nombre de commandes"""
        return len(list(self.bot.tree.walk_commands()))

    async def get_status_messages(self) -> list:
        """Génère la liste des messages de statut"""
        total_members = self.get_total_members()
        total_guilds = len(self.bot.guilds)
        total_channels = self.get_total_channels()
        total_commands = self.get_total_commands()
        uptime = self.get_uptime()
        
        # Calculer les membres en ligne (approximatif)
        online_members = 0
        for guild in self.bot.guilds:
            online_members += sum(1 for m in guild.members if m.status != discord.Status.offline)
        
        # Calculer les bots (sans doublons)
        total_bots = self.get_total_bots()
        
        # Calculer les utilisateurs réels (non-bots)
        real_users = total_members - total_bots
        
        statuses = [
            # Statistiques principales
            {
                "type": discord.ActivityType.watching,
                "name": f"{self.format_number(total_members)} membres"
            },
            {
                "type": discord.ActivityType.watching,
                "name": f"{self.format_number(total_guilds)} serveurs"
            },
            {
                "type": discord.ActivityType.watching,
                "name": f"{self.format_number(online_members)} membres en ligne"
            },
            {
                "type": discord.ActivityType.watching,
                "name": f"{self.format_number(real_users)} utilisateurs"
            },
            {
                "type": discord.ActivityType.watching,
                "name": f"{self.format_number(total_channels)} salons"
            },
            {
                "type": discord.ActivityType.playing,
                "name": f"{total_commands} commandes"
            },
            {
                "type": discord.ActivityType.watching,
                "name": f"Uptime: {uptime}"
            },
            # Stats fun
            {
                "type": discord.ActivityType.listening,
                "name": "/help pour l'aide"
            },
            {
                "type": discord.ActivityType.watching,
                "name": "Purity Bot"
            },
        ]
        
        return statuses

    @tasks.loop(seconds=30)  # Change toutes les 30 secondes
    async def update_status(self):
        await self.bot.wait_until_ready()
        try:
            statuses = await self.get_status_messages()
            
            if not statuses:
                return
            
            # Sélectionner le statut actuel
            current_status = statuses[self.status_index % len(statuses)]
            
            # Créer l'activité
            activity = discord.Activity(
                type=current_status["type"],
                name=current_status["name"]
            )
            
            await self.bot.change_presence(
                activity=activity,
                status=discord.Status.online
            )
            
            # Passer au statut suivant
            self.status_index += 1
            
        except Exception as e:
            print(f"{self.C.RED}[ERROR] {self.C.WHITE}Erreur lors de la mise à jour du statut: {e}")

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()
        print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Système de statut rotatif initialisé !")

async def setup(bot: commands.Bot):
    await bot.add_cog(RotatingStatus(bot))

