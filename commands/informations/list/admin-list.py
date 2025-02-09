from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class adminList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="all-admins", description="Afficher la liste de tout les membres avec la permissions administrateur")
    async def adminlist(self, interaction: discord.Interaction) -> None:
        check: bool = await check_perms(interaction, 1)
        if check == False:
            return
        
        await logs("admins-list", 1, interaction)

        adminsListed: list[str] = [f'{member.mention}`{member.id}`' for member in interaction.guild.members if member.guild_permissions.administrator]

        embed: embedBuilder = embedBuilder(
            title="`👤`・Liste des administrateurs",
            description="\n".join(adminsListed),
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(adminList(bot))