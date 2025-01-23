import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class jailConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="jail-config", description="Configurer la commande prison")
    async def jailconfig(self, interaction: discord.Interaction, role: discord.Role):
        if not await check_perms(interaction, 2):
            return
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['jail']['role'] = role.id
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed = embedBuilder(
            title="`🧱`・Prison",
            description=f"*Le role {role.mention} a bien été definit comme le role prison.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(jailConfig(bot))