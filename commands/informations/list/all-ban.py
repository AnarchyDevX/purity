import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.allBansView.precedentButton import precedentButtonBans
from views.allBansView.suivantButton import suivantButtonBans

class allBan(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    
    @app_commands.command(name="all-bans", description="Afficher la liste de tout les membres bannis")
    async def allbans(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 1): return
        banlist = [member async for member in interaction.guild.bans()]
        if banlist == []:
            embed = embedBuilder(
                title=f"`✨`・Liste des membres bannis",
                description=f"*Il n'y aucun membre banni sur le serveur.*",
                color=embed_color(),
                footer=footer()
            )
            return await interaction.response.send_message(embed=embed)
        
        banlist = [f"***{element.user.name}*** | `{element.user.id}`" for element in banlist]
        pages = [banlist[i:i + 50] for i in range(0, len(banlist), 50)]

        embed: embedBuilder = embedBuilder(
                title=f"`✨`・Liste des membres bannis",
                description="\n".join(pages[0]),
                color=embed_color(),
                footer=f"Page: {0 + 1}/{len(pages)}"
            )
        view = discord.ui.View(timeout=None)
        view.add_item(precedentButtonBans(0, pages))
        view.add_item(suivantButtonBans(0, pages))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(allBan(bot))