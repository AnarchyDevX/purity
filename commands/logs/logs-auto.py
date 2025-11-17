import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class logsAuto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="logs-auto", description="Crée les salons automatiquement et la configuration automatique")
    async def logsAuto(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2): return
        await interaction.response.defer()
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), 
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True) 
        }
        category = await interaction.guild.create_category(name="📂 logs", overwrites=overwrites)
        channels_name = ["ranklogs", "modlogs", "raidlogs", "voicelogs", "msglogs", "joinleavelogs"]
        guildJSON =  load_json_file(f'./configs/{interaction.guild.id}.json')
        for name in channels_name:
            channel = await category.create_text_channel(
                name=f"📂 {name}", 
                overwrites=overwrites
            )
            guildJSON['logs'][name]["alive"] = True
            guildJSON["logs"][name]['channel'] = channel.id

        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)

        embed = embedBuilder(
            title=f"`📂`・{lang('logs.autoTitle')}",
            description=f"*La configuration des logs automatiques est terminée.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(logsAuto(bot))