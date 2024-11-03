import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class badwordsAdd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="badwords-add", description="Ajouter un badword")
    async def setup(self, interaction: discord.Interaction, mot: str) -> None:
        if not await check_perms(interaction, 2):
            return 
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        badwordsList: list[str] = guildJSON['badwords']
        if mot in badwordsList:
            return await err_embed(
                interaction,
                title="Badword déja présent",
                description=f"Le mot `{mot}` est déja présent dans la liste des badwords."
            )
        
        badwordsList.append(mot)
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)

        embed = embedBuilder(
            title="`🛠️`・Badword ajouté",
            description=f"*Le mot `{mot}` à été ajouté dans la liste des badwords.*",
            color=embed_color(),
            footer=footer()
        )

        return await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(badwordsAdd(bot))