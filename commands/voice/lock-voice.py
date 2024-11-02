import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class lockVoice(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="voice-lock", description="Bloquer un salon vocal")
    async def voiceLock(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        lockeds: list[int] = guildJSON['lockedvoice']
        if channel.id in lockeds:
            return await err_embed(
                interaction, 
                title="Salon déjà lock",
                description=f"Le salon {channel.mention} est déjà lock"
            )
        
        lockeds.append(channel.id)
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed: embedBuilder = embedBuilder(
            title="`🔒`・Salon lock",
            description=f"*Le salon {channel.mention} est maintenant bloqué*",
            color=embed_color(),
            footer=footer(),
            fields={
                "`ℹ️`・Informations": (
                    "> *Uniquement des membre de la whitelist et de la ownerlist pourrons rejoindre ce salon vocal.*",
                    False
                )
            }
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(lockVoice(bot))