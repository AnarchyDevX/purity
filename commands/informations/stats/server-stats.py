import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class serverStats(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="stats-serveur", description="Afficher les stats actuels du serveur")
    async def statsserveur(self, interaction: discord.Interaction):

        online = sum(1 for member in interaction.guild.members if member.status == discord.Status.online)
        offline = sum(1 for member in interaction.guild.members if member.status == discord.Status.offline)
        idle = sum(1 for member in interaction.guild.members if member.status == discord.Status.idle)
        dnd = sum(1 for member in interaction.guild.members if member.status == discord.Status.dnd)

        embed = embedBuilder(
            title="`🏆`・Statistiques du serveur",
            description=(
                f"> `🟢`・**En ligne:** `{online}`\n"
                f"> `⚫`・**Hors Ligne:** `{offline}`\n"
                f"> `🟡`・**Inactif:** `{idle}`\n"
                f"> `🔴`・**Ne pas déranger:** `{dnd}`\n"
            ),
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(serverStats(bot))