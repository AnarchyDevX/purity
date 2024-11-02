from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.autoReactView.autoReactSelect import autoReactSelect

class autoReactRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        
    @app_commands.command(name="reaction-auto-remove", description="Supprimer une reaction automatique a un message")
    async def autoReactRemove(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        config = load_json_file(f"./configs/{interaction.guild.id}.json")
        if config['configuration']['autoreact'] == {}:
            return await err_embed(
                interaction,
                title="Aucune reaction automatique configurée",
                description="Il n'y a actuellement aucune configuration automatique configurée"
            )
        
        embed: embedBuilder = embedBuilder(
            title="`💈`・Gestion des réactions automatiques",
            description="*Merci de bien vouloir selectionner la reaction a réacion a supprimé*",
            color=embed_color(),
            footer=footer()
        )
        
        view = discord.ui.View(timeout=None)
        view.add_item(autoReactSelect(interaction.guild, interaction.user))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoReactRemove(bot))