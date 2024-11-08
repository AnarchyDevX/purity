import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class joinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="join-message", description="Ajouter un message a l'arrivée")
    @app_commands.choices(
        type=[
            app_commands.Choice(name="embed", value="embed"),
            app_commands.Choice(name="message", value="message")
        ],
        mention=[
            app_commands.Choice(name="oui", value="True"),
            app_commands.Choice(name="non", value="False")
        ]
    )
    async def joinMessage(self, interaction: discord.Interaction, type: str, channel: discord.TextChannel, mention: str):
            if not await check_perms(interaction, 2):
                return
            
            guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')

            if type == "embed":
                guildJSON['greeting']['type'] = 'embed'
                if mention == "True":
                    guildJSON['greeting']['mention'] = True
                else:
                    guildJSON['greeting']['mention'] = False
            elif type == "message":
                if mention == "True":
                    guildJSON['greeting']['mention'] = True
                else:
                    guildJSON['greeting']['mention'] = False
            guildJSON['greeting']['active'] = True
            guildJSON['greeting']['channel'] = channel.id
            json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
            embed = embedBuilder(
                title="`🖖`・Message de bienvenue",
                description=f"*Le message à bien été configurer.*",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🛠️`・Configuration": (
                        f'> `🪼`・**Type:** `{type}`\n'
                        f'> `📍`・**Mention:** `{"oui" if mention == "True" else "non"}`\n'
                        f'> `🪄`・**Salon:** {channel.mention}',
                        False
                    )
                }
            )
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(joinMessage(bot))