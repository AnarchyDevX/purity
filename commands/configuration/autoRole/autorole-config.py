import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.autoRole.autoRoleAdd import autoroleAddButton
from views.autoRole.autoRoleRemove import autoroleRemoveButton

class autoRoleList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="autorole-config", description="Configurer l'autorole")
    async def autoroleList(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON: Dict[str, Any] = load_json_file(f'./configs/{interaction.guild.id}.json')
        rolesList: list[str] = [f"<@&{roleId}> `{roleId}`" for roleId in guildJSON['configuration']['autorole']]
        embed: embedBuilder = embedBuilder(
            title="`✨`・Liste des roles ajoutés a l'arrivée",
            description=','.join(rolesList),
            footer=footer(),
            color=embed_color()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(autoroleAddButton(interaction.user.id, self.bot))
        view.add_item(autoroleRemoveButton(interaction.user.id, self.bot))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoRoleList(bot))