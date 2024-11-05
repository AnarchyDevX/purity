import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

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
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(onlyPicList(bot))