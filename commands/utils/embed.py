import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.embedView.sendButton import sendButton
from views.embedView.componentSelect import componentSelect
from views.embedView.componentResetSelect import componentResetSelect

class embed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="embed", description="Cree et envoyer un embed")
    async def embed(self, interaction: discord.Interaction) -> None:
        await logs("embed", 1, interaction)
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        embed: embedBuilder = embedBuilder(
            title="Titre",
            description="*Description*",
            color=embed_color()
        )
        view: discord.ui.View = discord.ui.View(timeout=None)
        view.add_item(componentSelect(interaction.user.id, self.bot))
        view.add_item(componentResetSelect(interaction.user.id, self.bot))
        view.add_item(sendButton(interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(embed(bot))
