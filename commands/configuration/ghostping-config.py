import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ghostpingView.add import addGhostPingButton
from views.ghostpingView.remove import removeGhostPingButton

class ghostpingConfig(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="ghostping-config", description="Afficher l'embed de configuration et de gestion des ghostping")
    async def ghostping(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        ghostpingList = guildJSON['ghostping']


        embed = embedBuilder(
            title="`👻`・Ghostping",
            description="\n".join(f'<#{channelId}> `{channelId}`' for channelId in ghostpingList),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(addGhostPingButton(self.bot, interaction.user.id))
        view.add_item(removeGhostPingButton(self.bot, interaction.user.id))
        return await interaction.response.send_message(embed=embed, view=view)
    
async def setup(bot):
    await bot.add_cog(ghostpingConfig(bot))