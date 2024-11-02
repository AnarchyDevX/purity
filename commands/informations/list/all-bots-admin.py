from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class allBotAdmin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


    @app_commands.command(name="all-bot-admin", description="Affiche tout les bots ayant la permissions administrateur")
    async def allBotAdmin(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 1)
        if check == False:
            return
        
        botAdminList: list[str] = [f'{member.mention}`{member.id}`' for member in interaction.guild.members if member.bot]
        embed: embedBuilder = embedBuilder(
            title="`✨`・Liste des bots avec les permissions administrateur",
            description='\n'.join(botAdminList),
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(allBotAdmin(bot))