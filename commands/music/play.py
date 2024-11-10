import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from functions.functions import *

class musicPlay(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="play", description="Jouer de la musique")
    async def mucisplay(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        voice_channel = interaction.user.voice.channel
        if not voice_channel:
            await interaction.followup.send("Tu dois être dans un canal vocal pour utiliser cette commande.")
            return
        voice_client = await voice_channel.connect()
        video_url = search_youtube(query)
        audio_url = get_audio_url(video_url)
        voice_client.play(discord.FFmpegPCMAudio(audio_url))
        embed = embedBuilder(
            title="`🎵`・En train de jouer",
            description=f"*Je suis en train de jouer*"
        )
        await interaction.followup.send(f"Je joue : {query}")
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(musicPlay(bot))