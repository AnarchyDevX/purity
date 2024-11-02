from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class allBot(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="all-bots", description="Afficher tout les bots presents sur le serveur")
    async def allbots(self, interaction: discord.Interaction) -> None:
        await logs("all-bots", 1, interaction)
        botsList: list = []
        for member in interaction.guild.members:
            if member.bot:
                botsList.append(f'> `✨`・**Nom:** `{member.name}`\n> `🆔`・**Id:** `{member.id}`\n> `🪄`・**Crée le:** `{format_date("all", member.created_at)}`\n> `➕`・**Rejoint le:** `{format_date("all", member.joined_at)}`\n')

        embed: embedBuilder = embedBuilder(
            title="`🛠️`・Bots présents sur le serveur",
            description="\n".join(botsList),
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(allBot(bot))