import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class find(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot =  bot

    @app_commands.command(name="find", description="Chercher si un membre est dans un salon vocal")
    async def setup(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice:
            return await err_embed(
                interaction,
                title="Membre non présent dans un salon vocal",
                description=f"Le membre {member.mention} n'est pas présent dans un salon vocal"
            )

        embed: embedBuilder = embedBuilder(
            title="`💈`・Recherche du membre dans un salon vocal",
            description=f"*Le membre {member.mention} est présent dans le salon vocal {member.voice.channel.mention}.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)    

async def setup(bot: commands.Bot):
    await bot.add_cog(find(bot))    