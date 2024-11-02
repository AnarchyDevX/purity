import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class inviteLink(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="invite-link", description="Obtenir le lien d'invitation du bot")
    async def inviteLink(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 3)
        if check == False:
            return
        
        embed: embedBuilder = embedBuilder(
            title="`🎃`・Lien d'invitation du bot",
            description=f"*Voici le lien d'inviation du bot:* \n> https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8",
            footer=footer(),
            color=embed_color(),
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(inviteLink(bot))
