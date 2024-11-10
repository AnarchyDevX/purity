import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class soutienPanel(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="soutien-panel", description="Affiche la configuration du role soutien")
    async def soutienPanel(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2): return
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        embed = embedBuilder(
            title="`🛠️`・Panel soutien",
            color=embed_color(),
            footer=footer(),
            fields={
                "`👘`・actif": (
                    "`oui`" if guildJSON['soutien']['active'] == True else "`non`",
                    True
                ),
                "`🪄`・status": (
                    f"`{guildJSON['soutien']['needed']}`",
                    True
                ),
                "`🛡️`・role ajouté": (
                    f"<@&{guildJSON['soutien']['role']}>" if guildJSON["soutien"]['role'] != None else "`non définit`",
                    True
                )
            }
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(soutienPanel(bot))