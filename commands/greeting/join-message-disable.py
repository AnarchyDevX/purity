import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class joinMessageDisable(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="join-message-disable", description="Désactiver le message de bienvenue")
    async def joinmessagedisable(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        guildJSON['greeting']['active'] = False
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`🖖`・Message de bienvenue",
            description=f"*Le message à bien été désactivé.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(joinMessageDisable(bot))