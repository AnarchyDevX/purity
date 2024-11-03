import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class badwordsRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="badwords-remove", description="Retirer un badword")
    async def setup(self, interaction: discord.Interaction, mot: str) -> None:
        if not await check_perms(interaction, 2):
            return 
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        badwordsList: list[str] = guildJSON['badwords']
        if mot not in badwordsList:
            return await err_embed(
                interaction,
                title="Badword non présent",
                description=f"Le mot `{mot}` n'est pas présent dans la liste des badwords."
            )
        
        badwordsList.remove(mot)
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)

        embed = embedBuilder(
            title="`🛠️`・Badword retiré",
            description=f"*Le mot `{mot}` à été retiré de la liste des badwords.*",
            color=embed_color(),
            footer=footer()
        )

        return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(badwordsRemove(bot))