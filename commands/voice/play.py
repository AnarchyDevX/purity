import yt_dlp
import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal, Dict, Any
from core.embedBuilder import embedBuilder
from functions.functions import logs, err_embed,embed_color, footer

class musicPlay(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.voice_client: None = None  
    
    def get_youtube_url(self, song_name: str) -> (tuple | tuple[Literal[False], Literal[False]]):
        ydl_opts: Dict[str, Any] = {
            'format': 'bestaudio',
            'nocache': True  
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info: Any | dict[str, Any] | None = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if info['entries']:
                return info['entries'][0]['url'], info['entries'][0]['title']
            return False, False

    @app_commands.command(name="music-play", description="Jouer de la musique dans un salon vocal")
    async def music_play(self, interaction: discord.Interaction, name: str) -> None:
        await logs("music-play", 1, interaction)
        await interaction.response.defer()
        if not interaction.user.voice:
            return await err_embed(
                interaction,
                title="Salon manquant",
                description=f"Vous n'êtes pas présent dans un salon vocal.",
                followup=True
            )

        if not interaction.guild.voice_client:
            self.voice_client = await interaction.user.voice.channel.connect()
        else:
            self.voice_client = interaction.guild.voice_client
            if self.voice_client.is_playing():
                self.voice_client.stop()

        url, title = self.get_youtube_url(name)
        if not url:
            return await interaction.followup.send(content="*Je n'arrive pas à trouver la musique que vous recherchez*", ephemeral=False)
        
        self.voice_client.play(discord.FFmpegPCMAudio(url, executable='music-convert.exe'), after=lambda e: print(f'Lecture terminée : {e}'))
        embed: embedBuilder = embedBuilder(
            title=f"`🎧`・En train de jouer",
            description=f"*En train de jouer `{title}` dans {interaction.user.voice.channel.mention}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(musicPlay(bot))
