import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceUnlockAll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-unlock-all", description="Débloquer tout les salons vocaux du serveur")
    async def voiceUnlockAll(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        lockedList: list[int] = guildJSON['lockedvoice']
        for channel in interaction.guild.voice_channels:
            if channel.id not in lockedList:
                pass
            else:
                lockedList.remove(channel.id)
                
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        embed: embedBuilder = embedBuilder(
            title="`🔇`・Tout les salons sont unlock",
            description=f"*`{len(interaction.guild.voice_channels)}` salon vocaux on été unlock.*",
            color=embed_color(),
            footer=()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceUnlockAll(bot))