import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class unlockVoice(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="voice-unlock", description="Débloquer un salon vocal")
    async def voiceLock(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        lockeds: list[int] = guildJSON['lockedvoice']
        if channel.id not in lockeds:
            return await err_embed(
                interaction, 
                title="Salon déjà non lock",
                description=f"Le salon {channel.mention} n'est pas lock"
            )
        
        lockeds.remove(channel.id)
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        embed: embedBuilder = embedBuilder(
            title="`🔒`・Salon unlock",
            description=f"*Le salon {channel.mention} est maintenant débloqué*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(unlockVoice(bot))