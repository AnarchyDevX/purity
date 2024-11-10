import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class soutienDisable(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="soutien-disable", description="Désactiver le role soutien")
    async def soutienDisable(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2): return
        guildJSON = load_json_file(f"./guilds/{interaction.guild.id}.json")
        guildJSON['soutien']['active'] = False
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`📌`・Role soutien",
            description=f"*Le role ajouté au soutien a été désactivé*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(soutienDisable(bot))