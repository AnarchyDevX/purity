import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class antiChannelConfig(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="antiraid-antichannel", description="Configurer l'antichannel")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="all", value="all"),
            app_commands.Choice(name="crée", value="create"),
            app_commands.Choice(name="modifié", value="edit"),
            app_commands.Choice(name="supprimé", value="delete")
        ],
        status=[
            app_commands.Choice(name="on", value="True"),
            app_commands.Choice(name="off", value="False")
        ]
    )
    async def antichannelConfig(self, interaction: discord.Interaction, option: str, status: str):
        if not await check_perms(interaction, 2): return

        status = True if status == "True" else False

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if option == "all":
            guildJSON['antiraid']["channels"]['create'] = status
            guildJSON['antiraid']["channels"]['edit'] = status
            guildJSON['antiraid']["channels"]['delete'] = status
        else:
            guildJSON['antiraid']["channels"][option] = status

        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        if option == "all":
            title = "all"
        elif option == "create":
            title = "crée"
        elif option == "edit":
            title = "modifié"
        elif option == "delete":
            title == "supprimé"

        embed: embedBuilder = embedBuilder(
            title=f"`🛡️`・Antichannel {title} {'activé' if status == True else 'désactivé'}",
            description=f"*L'antichannel {title} à bien été {'activé' if status == True else 'désactivé'}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(antiChannelConfig(bot))