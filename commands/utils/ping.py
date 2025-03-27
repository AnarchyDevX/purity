import time
import requests
import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="ping", description="Afficher la latence du bot")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("En train d'évaluer la latence...", ephemeral=True)

        now = time.time()
        message = await interaction.followup.send(content="...", ephemeral=True)
        editsLatency = ((time.time() - now) * 1000) - (self.bot.latency * 1000)
        
        embed = embedBuilder(
            title="`🪄`・Latence du bot",
            description=(
                f"`✨`・ **Latence du bot:** `{round(self.bot.latency * 1000)} ms`\n"
                f"`🖊️`・ **Latence des edits:** `{round(editsLatency)} ms`\n"
            ),
            color=embed_color(),
            footer=footer()
        )
        await message.edit(content=None, embed=embed)  

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCommand(bot))
