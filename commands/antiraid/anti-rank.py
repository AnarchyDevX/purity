import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class antiRankConfdif(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="antiraid-antirank", description="Configurer l'antirank")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="all", value="all"),
            app_commands.Choice(name="ajout", value="up"),
            app_commands.Choice(name="retrait", value="down")
        ],
        status=[
            app_commands.Choice(name="on", value="True"),
            app_commands.Choice(name="off", value="False")
        ]
    )
    async def antiRankConfdif(self, interaction: discord.Interaction, option: str, status: str):
        if not await check_perms(interaction, 2): return

        status = True if status == "True" else False

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if option == "all":
            guildJSON['antiraid']["rank"]['up'] = status
            guildJSON['antiraid']["rank"]['down'] = status
        else:
            guildJSON['antiraid']["roles"][option] = status

        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        if option == "all":
            title = "all"
        else:
            title == option

        embed: embedBuilder = embedBuilder(
            title=f"`🛡️`・Antirank {'activé' if status == True else 'désactivé'}",
            description=f"*L'antirank {title} à bien été {'activé' if status == True else 'désactivé'}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(antiRankConfdif(bot))