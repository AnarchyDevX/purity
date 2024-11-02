import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class autoRoleList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="autorole-list", description="Afficher tout les rôles ajoutés a l'arrivée")
    async def autoroleList(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON: Dict[str, Any] = load_json_file(f'./configs/{interaction.guild.id}.json')
        rolesList: list[str] = [f"<@&{roleId}>" for roleId in guildJSON['configuration']['autorole']]
        embed: embedBuilder = embedBuilder(
            title="`✨`・Liste des roles ajoutés a l'arrivée",
            description=','.join(rolesList),
            footer=footer(),
            color=embed_color()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoRoleList(bot))