import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceLockAll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-lock-all", description="Bloquer tout les salons vocaux du serveur")
    async def voiceLockAll(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        lockedList: list[int] = guildJSON['lockedvoice']
        for channel in interaction.guild.voice_channels:
            if channel.id in lockedList:
                pass
            else:
                lockedList.append(channel.id)
                
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        embed: embedBuilder = embedBuilder(
            title="`🔇`・Tout les salons sont lock",
            description=f"*`{len(interaction.guild.voice_channels)}` salon vocaux on été lock.*",
            color=embed_color(),
            footer=()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceLockAll(bot))