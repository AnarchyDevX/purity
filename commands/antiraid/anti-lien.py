import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class antiLienConfig(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="antiraid-antilien", description="Activer / désactiver l'antilien")
    @app_commands.choices(
        status=[
            app_commands.Choice(name="on", value="True"),
            app_commands.Choice(name="off", value="False")
        ]
    )
    async def antiLienConfig(self, interaction: discord.Interaction, status: str):
        if not await check_perms(interaction, 2): return
        status = True if status == "True" else False
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['antiraid']['antilien'] = status
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed: embedBuilder = embedBuilder(
            title=f"`🛡️`・Antilien {'activé' if status == True else 'désactivé'}",
            description=f"*L'antilien est désormais **{'activé' if status == True else 'désactivé'}**.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(antiLienConfig(bot))