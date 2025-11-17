import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceMoveAll(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-move-all", description="Permet de déplacer tout les membre en vocal dans votre salon vocal actuel")
    async def voicemoveall(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not await check_perms(interaction, 2): return
        if not interaction.user.voice:
            return await err_embed(
                interaction,
                title="Salon vocal manquant",
                description=f"Vous devez vous meme etre présent dans un salon vocal.",
                followup=True
            )
        
        
        succes = 0
        failed = 0
        for member in interaction.guild.members:
            if member.voice:
                if member.voice.channel == interaction.user.voice.channel:
                    continue
                try:
                    await member.move_to(interaction.user.voice.channel)
                    succes += 1
                except discord.Forbidden:
                    # Bot n'a pas les permissions
                    failed += 1
                except discord.HTTPException:
                    # Erreur Discord API
                    failed += 1
                await asyncio.sleep(0.5)

        embed = embedBuilder(
            title="`🔊`・Move all",
            description=f"*Tout les membres présent en vocal ont été déplacé dans le salon {interaction.user.voice.channel.mention}.*",
            color=embed_color(),
            footer=footer(),
            fields={
                f"`📜`・Informations sur le déplacement": (
                    f"> `🟢`・**Déplacé:** `{succes}`\n"
                    f"> `🔴`・**Non déplacé:** `{failed}`\n",
                    False
                )
            }
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(voiceMoveAll(bot))