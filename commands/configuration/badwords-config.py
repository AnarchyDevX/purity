import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.badwords.badwordAdd import badwordsAddButton
from views.badwords.badwordRemove import badwordsRemoveButton

class badwordList(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="badwords-config", description="Afficher tout les badwords configurés")
    async def badwordsList(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        await interaction.response.defer(ephemeral=True)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        badwords = ", ".join(guildJSON['badwords'])

        embed: embedBuilder = embedBuilder(
            title="`🧪`・Badwords",
            description=(
                f"> `🪄`・**Total:** `{len(guildJSON['badwords'])}`\n"
                f"> `📜`・**Liste:** ```{badwords}```\n"
            ),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(badwordsAddButton(interaction.user.id))
        view.add_item(badwordsRemoveButton(interaction.user.id))
        return await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(badwordList(bot))