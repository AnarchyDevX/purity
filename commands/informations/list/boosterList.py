import discord
from functions.functions import *
from discord import app_commands
from discord.ext import commands
from core.embedBuilder import embedBuilder

class boosterList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="all-booster", description="Afficher tout les membre boostant le serveur")
    async def booterList(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 1)
        if check == False:
            return
        
        boostList: list[str] = [f'{member.mention}`{member.id}`' for member in interaction.guild.premium_subscribers]

        embed: embedBuilder = embedBuilder(
            title="`🔮`・Liste des booster du serveur",
            description='\n'.join(boostList),
            footer=footer(),
            color=embed_color()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(boosterList(bot))