import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class logsPanel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="logs-panel", description="Afficher la configuration actuelle des logs")
    async def logspanel(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON =  load_json_file(f'./configs/{interaction.guild.id}.json')
        
        modsLogs = guildJSON['logs']['modlogs']
        msgLogs = guildJSON['logs']['msglogs']
        raidlogs = guildJSON['logs']['raidlogs']
        voicelogs = guildJSON['logs']['voicelogs']
        ranklogs = guildJSON['logs']['ranklogs']
        joinleaveLogs = guildJSON['logs']['joinleavelogs']

        embed: embedBuilder = embedBuilder(
            title="`📂`・Configuration actuelle des logs",
            color=embed_color(),
            footer=footer(),
            fields={
                "`📂`・Modération": (
                    f"<#{modsLogs['channel']}>" if modsLogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Messages": (
                    f"<#{msgLogs['channel']}>" if msgLogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Raids": (
                    f"<#{raidlogs['channel']}>" if raidlogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Vocale": (
                    f"<#{voicelogs['channel']}>" if voicelogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Ranks": (
                    f"<#{ranklogs['channel']}>" if ranklogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Joins et Leave": (
                    f"<#{joinleaveLogs['channel']}>" if joinleaveLogs['alive'] == True else "`désactivées`",
                    True
                ),
            }
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(logsPanel(bot))