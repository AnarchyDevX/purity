import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceMove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-move", description="Déplacer un membre vocal dans votre salon vocal actuel")
    async def voicemoove(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await logs("voice-move", 1, interaction)
        check: bool = await check_perms(interaction, 1)
        if check == False:
            return 
        if interaction.user == member:
            return await err_embed(
                interaction,
                title="Membre invalide",
                description=f"Vous ne pouvez pas vous déplacer vous même."
            )
        
        if not interaction.user.voice:
            return await err_embed(
                interaction,
                title="Salon manquant",
                description=f"Vous devez être présent dans un salon vocal."
            )
        
        if not member.voice:
            return await err_embed(
                interaction,
                title="Salon manquant",
                description=f"Le membre {member.mention} n'est pas présent dans un salon vocal."
            )
        
        try:
            await member.move_to(interaction.user.voice.channel)
        except Exception:
            return await err_embed(
                interaction,
                title="Impossible de déplacer le membre",
                description=f"Je n'ai pas réussi à déplacer le membre {member.mention}"
            )
        
        embed: embedBuilder = embedBuilder(
            title="`✅`・Membre déplacé",
            description=f"*Le membre {member.mention} à été déplacer avec succès dans le salon {interaction.user.voice.channel.mention}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceMove(bot))