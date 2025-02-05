import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.whitelist.add import whitelistAddButton
from views.whitelist.remove import whitelistRemoveButton

class whitelistList(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="whitelist-panel", description="Gerer la whitelist.")
    async def ownerlist(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        whitelist = guildJSON['whitelist']
        formatted = [f'<@{memberId}> `{memberId}`' for memberId in whitelist]
        embed = embedBuilder(
            title="`📜`・Whitelist",
            description='\n'.join(formatted),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(whitelistAddButton(self.bot, interaction.user.id))
        view.add_item(whitelistRemoveButton(self.bot, interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(whitelistList(bot))