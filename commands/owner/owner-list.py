import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class ownerList(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="owner-list", description="Afficher la liste des membre présents dans la liste des owners")
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
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ownerList(bot))