import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.onlyPicView.add import addButtonOnlypic
from views.onlyPicView.remove import removeButtonOnlypic

class onlyPicList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="onlypic-list", description="Afficher tout les salons ou l'onlypic est activé")
    async def onlypiclist(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2): return
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        onlypicList = [f"<#{channelId}> `{channelId}`" for channelId in guildJSON['onlypic']]

        embed = embedBuilder(
            title="`🥏`・Onlypic",
            description="\n".join(onlypicList),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(addButtonOnlypic(self.bot, interaction.user.id))
        view.add_item(removeButtonOnlypic(self.bot, interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(onlyPicList(bot))