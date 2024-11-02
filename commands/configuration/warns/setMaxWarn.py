import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class setMaxWarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="set-max-warn", description="Configurer le nombre maximal de warn avant l'application de la sanction")
    async def setMaxWarn(self, interaction: discord.Interaction, amount: int):
        check = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['warndb']['maxwarn'] = amount
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed = embedBuilder(
            title="`🛠️`・Configuration des warn",
            description=f"*Le nombre de warn maximal avant application de la sanction est `{amount} warn`*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(setMaxWarn(bot))