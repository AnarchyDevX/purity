import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class antiraidAll(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="antiraid-all", description="Activé / Désactive l'antiraid")
    @app_commands.choices(
        status=[
            app_commands.Choice(name="on", value="True"),
            app_commands.Choice(name="off", value="False")
        ]
    )
    async def antiraidall(self, interaction: discord.Interaction, status: str):
        if not await check_perms(interaction, 2):
            return
        status = True if status == "True" else False
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['antiraid']['antilien'] = status
        guildJSON['antiraid']['antibot'] = status
        guildJSON['antiraid']['badwords'] = status
        guildJSON['antiraid']['webhook'] = status
        guildJSON['antiraid']['channels']['create'] = status
        guildJSON['antiraid']['channels']['edit'] = status
        guildJSON['antiraid']['channels']['delete'] = status
        guildJSON['antiraid']['roles']['create'] = status
        guildJSON['antiraid']['roles']['edit'] = status
        guildJSON['antiraid']['roles']['delete'] = status
        guildJSON['antiraid']['rank']['up'] = status
        guildJSON['antiraid']['rank']['down'] = status
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed = embedBuilder(
            title="`🛡️`・Antiraid all",
            description=f"Le systeme d'antiraid a completement été activé",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(antiraidAll(bot))