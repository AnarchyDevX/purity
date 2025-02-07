import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class serverInfo(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="serveur-info", description="Afficher les informations relatives au serveur")
    async def serverinfo(self, interaction: discord.Interaction):
        embed = embedBuilder(
            title="`🪡`・Informations du serveur",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🌍`・Informations globales": (
                    f"`🎟️`・**Nom:** `{interaction.guild.name}`\n"
                    f"`👤`・**Membres:** `{interaction.guild.member_count}`\n"
                    f"`🔮`・**Boosts:** `{interaction.guild.premium_subscription_count}`\n"
                    f"`✨`・**Crée le:** `{format_date('all', interaction.guild.created_at)}`\n"
                    f"`👑`・**Propriétaire:** {interaction.guild.owner.mention} `{interaction.guild.owner.id}`",
                    False
                ),
                "`🛠️`・Informations relatives": (
                    f"`📜`・**Salons:** `{len(interaction.guild.channels)}`\n"
                    f"`💭`・**Textuel:** `{len(interaction.guild.text_channels)}`\n"
                    f"`🔊`・**Vocals:** `{len(interaction.guild.voice_channels)}`",
                    False
                )
            },
            thumbnailUrl=interaction.guild.icon,
            imageUrl=interaction.guild.banner
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(serverInfo(bot))
