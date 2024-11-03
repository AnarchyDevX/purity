import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class badwordList(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="badwords-list", description="Afficher tout les badwords configurés")
    async def badwordsList(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
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

        return await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(badwordList(bot))