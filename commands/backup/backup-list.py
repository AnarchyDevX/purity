import os
import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class backupList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="backup-list", description="Afficher la liste des backups enregistrée dans le bot")
    async def backupList(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 3): return

        user_backup_dir = f'./backups/{interaction.user.id}'
        
        # Vérifier si le dossier existe, sinon retourner une liste vide
        if not os.path.exists(user_backup_dir):
            embed = embedBuilder(
                title="`📜`・Liste des backups",
                description="Aucune backup enregistrée.",
                color=embed_color(),
                footer=footer()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        nameList = [name.split(".")[0] for name in os.listdir(user_backup_dir) if name.endswith('.json')]
        
        if not nameList:
            embed = embedBuilder(
                title="`📜`・Liste des backups",
                description="Aucune backup enregistrée.",
                color=embed_color(),
                footer=footer()
            )
        else:
            embed = embedBuilder(
                title="`📜`・Liste des backups",
                description="\n\n".join('`' + name + '`' for name in nameList),
                color=embed_color(),
                footer=footer()
            )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(backupList(bot))