import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import *
from views.helpView.select import selectHelp

class helpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Afficher le panel d'aide")
    async def helpcommand(self, interaction: discord.Interaction):
        embed  = embedBuilder(
            title="`🪄`・Panel d'aide",
            description=f"> *Voici le panel d'aide du bot {self.bot.user.mention}*\n\n> *Utilisez les menu deroulant pour afficher les differentes options*\n\n```[] = Obligatoire \n() = Optionnel```",
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(selectHelp(interaction.user.id, self.bot))
        return await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(helpCommand(bot))