import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class soutienEnable(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="soutien-enable", description="Activé le role soutien")
    async def soutienEnabel(self, interaction: discord.Interaction, status: str, role: discord.Role):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        guildJSON['soutien']['active'] = True
        guildJSON['soutien']['needed'] = status
        guildJSON['soutien']['role'] = role.id
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`✨`・Role soutien",
            description=f"*Le role soutien a été activé*",
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(soutienEnable(bot))