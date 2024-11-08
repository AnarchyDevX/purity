import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class joinMessagePanel(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="join-message-panel", description="Afficher la configuration du message d'arrivée")
    async def joinMessagePanel(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2): return

        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        greeting = guildJSON['greeting']
        embed = embedBuilder(
            title="`🖖`・Message de bienvenue",
            color=embed_color(),
            footer=footer(), 
            fields={
                "`📍`・Actif": (
                    "`oui`" if greeting['active'] == True else "`non`", 
                    True
                ),
                "`🪼`・Type": (
                    "`message`" if greeting['type'] == "message" else "`embed`", 
                    True
                ),
                "`🪄`・Salon": (
                    f"<#{greeting['channel']}>" if greeting['channel'] != None else "`non définit`", 
                    True
                ),
                "`📢`・Mention": (
                    f"`non`" if greeting['mention'] == False else "`oui`", 
                    True
                )
            }
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(joinMessagePanel(bot))