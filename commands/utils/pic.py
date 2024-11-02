import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class pic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="pic", description="Afficher la photo d'utilisateur d'un membre")
    async def pic(self, interaction: discord.Interaction, member: discord.Member):
        embed: embedBuilder = embedBuilder(
            title="`🖼️`・Photo d'utilisateur",
            imageUrl=member.avatar,
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(pic(bot))