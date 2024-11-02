import json
from typing import Dict, Any
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class logsMsg(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="logs-messages", description="Activer / Désactiver les logs des messages")
    @app_commands.choices(
        alive=[
            app_commands.Choice(name="oui", value="yes"),
            app_commands.Choice(name="non", value="no")
        ]
    )
    async def logsMsg(self, interaction: discord.Interaction, alive: str, channel: discord.TextChannel = None) -> None:
        check: bool = await check_perms(interaction, 2)
        await logs("logs-messages", 1, interaction)
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
            guildJSON['logs']['msglogs']['alive'] = False
            json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
            embed: embedBuilder = embedBuilder(
                title="`✅`・Logs des messages",
                description=f"*Les logs des messages ont été désactivées*",
                color=embed_color(),
                footer=footer()
            )    
            return await interaction.response.send_message(embed=embed)
        elif alive == "yes" and isinstance(channel, discord.TextChannel):
            guildJSON['logs']['msglogs']['alive'] = True
            guildJSON['logs']['msglogs']['channel'] = channel.id
            json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
            embed: embedBuilder = embedBuilder(
                title="`✅`・Logs des messages",
                description=f"*Les logs des messages ont été activées dans le salon {channel.mention}.*",
                color=embed_color(),
                footer=footer()
            )    
            return await interaction.response.send_message(embed=embed)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(logsMsg(bot))