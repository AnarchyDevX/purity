import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class logsAuto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="logs-auto", description="Crée les salons automatiquement et la configuration automatique")
    async def logsAuto(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2): return
        category = await interaction.guild.create_category(name="📂 logs", overwrites={interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False)})
        channelsName = [ "📂 ranks", "📂 mods", "📂 raid", "📂 vocal", "📂 msg", "📂 joins leave"]
        for element in channelsName:
            try: await category.create_text_channel(name=element)
            except Exception: continue

        
