from typing import Dict, Any
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class logsAll(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="logs-all", description="Configurer toutes les logs dans le meme salon")
    @app_commands.choices(
        alive=[
            app_commands.Choice(name="oui", value="yes"),
            app_commands.Choice(name="non", value="no")
        ]
    )
    async def logsall(self, interaction: discord.Interaction, alive: str, channel: discord.TextChannel) -> None:
        await logs("logs-all", 1, interaction)
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return

        if alive == "yes" and channel == None:
            return await err_embed(
                interaction,
                title="Salon manquant",
                description="Si vous voulez activer les logs, vous devez fournir un salon valide."
            )
        
        guildJSON: Dict[str, Any] = load_json_file(f"./configs/{interaction.guild.id}.json")
        if alive == "no":
            guildJSON['logs']['ranklogs']['alive'] = False
            guildJSON['logs']['modlogs']['alive'] = False
            guildJSON['logs']['msglogs']['alive'] = False
            guildJSON['logs']['raidlogs']['alive'] = False
            guildJSON['logs']['voicelogs']['alive'] = False
            guildJSON['logs']['joinleavelogs']['alive'] = False
            json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
            embed: embedBuilder = embedBuilder(
                title="`✅`・Logs all",
                description=f"*Toutes les logs ont été désactivée.*",
                footer=footer(),
                color=embed_color()
            )    
            return await interaction.response.send_message(embed=embed)

        if alive == "yes":
            guildJSON['logs']['ranklogs']['alive'] = True
            guildJSON['logs']['modlogs']['alive'] = True
            guildJSON['logs']['msglogs']['alive'] = True
            guildJSON['logs']['raidlogs']['alive'] = True
            guildJSON['logs']['voicelogs']['alive'] = True
            guildJSON['logs']['joinleavelogs']['alive'] = True
            guildJSON['logs']['ranklogs']['channel'] = channel.id
            guildJSON['logs']['modlogs']['channel'] = channel.id
            guildJSON['logs']['msglogs']['channel'] = channel.id
            guildJSON['logs']['raidlogs']['channel'] = channel.id
            guildJSON['logs']['voicelogs']['channel'] = channel.id
            guildJSON['logs']['joinleavelogs']['channel'] = channel.id

            json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
            embed: embedBuilder = embedBuilder(
                title="`✅`・Logs all",
                description=f"*Toutes les logs ont été activées dans le salon {channel.mention}.*",
                footer=footer(),
                color=embed_color()
            )    
            return await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(logsAll(bot))