import discord
from functions.functions import *
from discord import app_commands
from discord.ext import commands
from core.embedBuilder import embedBuilder

class roleInformations(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="role-info", description="Afficher les informations d'un role")
    async def roleInfo(self, interaction: discord.Interaction, role: discord.Role):
        embed: embedBuilder = embedBuilder(
            title=f"`🧬`・Informations sur le role {role.name}",
            description=(
                f"> `🪄`・**Nom:** `{role.name}`\n"
                f"> `🆔`・**Id:** `{role.id}`\n"
                f"> `✨`・**Mention:** {role.mention}\n"
                f"> `🪡`・**Position:** `{role.position}`\n"
                f"> `➕`・**Créé le:** `{format_date('all', role.created_at)}`\n"
                f"> `🎨`・**Couleur:** `{role.color}`\n"
                f"> `🛠️`・**Permissions admin:** `{'oui' if role.permissions.administrator == True else 'non'}`\n"
            ),
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(roleInformations(bot))