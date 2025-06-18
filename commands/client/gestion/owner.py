import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ownerlist.add import ownerAddButton
from views.ownerlist.remove import ownerRemoveButton

class ownerList(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="owner-panel", description="Gêrer les owners bot")
    async def ownerlist(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 3):
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        ownerlist = guildJSON['ownerlist']
        formatted = [f'<@{memberId}> `{memberId}`' for memberId in ownerlist]
        embed = embedBuilder(
            title="`📜`・Liste des owners bot",
            description='\n'.join(formatted),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(ownerAddButton(self.bot, interaction.user.id))
        view.add_item(ownerRemoveButton(self.bot, interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ownerList(bot))