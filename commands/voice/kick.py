import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceKick(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-kick", description="Expulser un membre d'un salon vocal")
    async def voiceKick(self, interaction: discord.Interaction, member: discord.Member):
        check: bool = await check_perms(interaction, 1)
        if check == False:
            return
        
        if not member.voice:
            return await err_embed(
                interaction,
                title="Connection manquante",
                description=f"Le membre {member.mention} n'est pas présent dans un salon vocal."
            )
        
        try:
            await member.move_to(None)
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Impossible d'expulser le membre",
                description=f"Je n'ai pas réussi à expulser le membre {member.mention} de {member.voice.channel.mention}. Permission manquante."
            )
        except discord.HTTPException:
            return await err_embed(
                interaction,
                title="Impossible d'expulser le membre",
                description=f"Je n'ai pas réussi à expulser le membre {member.mention} de {member.voice.channel.mention}. Erreur Discord API."
            )
        
        embed: embedBuilder = embedBuilder(
            title="`🎗️`・Membre expulsé",
            description=f"Le membre {member.mention} à bien été expulser du salon {member.voice.channel.mention}.",
            footer=footer(),
            color=embed_color()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceKick(bot))