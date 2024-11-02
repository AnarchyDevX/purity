from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.roleReactionView.roleReactionSelect import roleReactSelect

class roleReactRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        
    @app_commands.command(name="role-reaction-remove", description="Supprimer un role reaction")
    async def roleReactRemove(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        config = load_json_file(f"./configs/{interaction.guild.id}.json")
        if config['configuration']['autoreact'] == {}:
            return await err_embed(
                interaction,
                title="Aucun role reaction configurée",
                description="Il n'y a actuellement aucune configuration de role reaction"
            )
        
        embed: embedBuilder = embedBuilder(
            title="`💈`・Gestion des role reaction",
            description="*Merci de bien vouloir selectionner la configuration de role reaction a supprimé*",
            color=embed_color(),
            footer=footer()
        )
        
        view = discord.ui.View(timeout=None)
        view.add_item(roleReactSelect(interaction.guild, interaction.user))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(roleReactRemove(bot))