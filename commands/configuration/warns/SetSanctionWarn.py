import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class setSanctionWarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="set-sanction-warn", description="Configurer la sanction lors du dépassement du nombre maximal de warn")
    @app_commands.choices(
        sanction=[
            app_commands.Choice(name="bannisement", value="ban"),
            app_commands.Choice(name="expulsion", value="kick")
        ]
    )
    async def setSanctionWarn(self, interaction: discord.Interaction, sanction: str):
        check = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['warndb']['sanction'] = sanction
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed = embedBuilder(
            title="`🛠️`・Configuration des warn",
            description=f"*Dès qu'un membre atteindra le nombre maximal de warn, il sera **{'banni' if sanction == 'ban' else 'expulser'}** du serveur*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(setSanctionWarn(bot))