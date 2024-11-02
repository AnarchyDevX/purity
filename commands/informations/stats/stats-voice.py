import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class statsVoice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="stats-voice", description="Afficher les statistiques vocales du serveur")
    async def statsVoice(self, interaction: discord.Interaction):
        
        connected: int = sum(1 for member in interaction.guild.members if member.voice != None)
        mute: int = sum(1 for member in interaction.guild.members if member.voice != None and member.voice.self_mute == True)
        deaf: int = sum(1 for member in interaction.guild.members if member.voice != None and member.voice.self_deaf == True)
        muted: int = sum(1 for member in interaction.guild.members if member.voice != None and member.voice.mute == True)
        deafed: int = sum(1 for member in interaction.guild.members if member.voice != None and member.voice.deaf == True)
        camera: int = sum(1 for member in interaction.guild.members if member.voice != None and member.voice.self_video == True)
        stream: int = sum(1 for member in interaction.guild.members if member.voice != None and member.voice.self_stream == True)

        embed: embedBuilder = embedBuilder(
            title="`🏆`・Statistiques vocales du serveur",
            description=(
                f"> `🟢`・**Connecté:** `{connected}/{interaction.guild.member_count}`\n"
                f"> `🔇`・**Muet:** `{mute}/{connected}`\n"
                f"> `🎧`・**Sourdine:** `{deaf}/{connected}`\n"
                f"> `🔈`・**Mis en Muet:** `{muted}/{connected}`\n"
                f"> `😴`・**Mis en Sourdine:** `{deafed}/{connected}`\n"
                f"> `📷`・**Caméra:** `{camera}/{connected}`\n"
                f"> `📽️`・**Steaming:** `{stream}/{connected}`\n"
            ),
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(statsVoice(bot))