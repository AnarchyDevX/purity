import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="ping", description="show bot latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        embed: embedBuilder = embedBuilder(
            title="`🪄`・Latence du bot",
            description=f"La latence du bot est de `{round(self.bot.latency * 1000)} ms`",
            color=embed_color(),
            footer=footer()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCommand(bot)) 