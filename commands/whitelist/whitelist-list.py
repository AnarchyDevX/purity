import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class whitelistList(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="whitelist-list", description="Afficher la liste des membre présents dans la whitelist")
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
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(whitelistList(bot))