import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceAft(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-afk", description="Déplacer un membre vers le salon vocal AFK")
    async def voiceAfk(self, interaction: discord.Interaction, member: discord.Member):
        check: bool = await check_perms(interaction, 1)
        if check == False:
            return
        
        if not member.voice:
            return await err_embed(
                interaction,
                title="Connection manquante",
                description=f"Le membre {member.mention} n'est pas présent dans un salon vocal."
            )

        if interaction.guild.afk_channel == None:
            return await err_embed(
                interaction,
                title="Salon afk non définit",
                description=f"Le salon afk n'est pas définit je ne peux donc pas deplacer {member.mention} dans ce dernier."
            )

        try:
            await member.move_to(interaction.guild.afk_channel)
        except Exception:
            return await err_embed(
                interaction,
                title="Impossible de deplacer le membre",
                description=f"Je n'ai pas réussi a déplacer le membre {member.mention} dans le salon vocal {interaction.guild.afk_channel.mention}."
            )
        
        embed: embedBuilder = embedBuilder(
            title="`😴`・Afk",
            description=f"*Le membre {member.mention} à bien été déplacer dans {interaction.guild.afk_channel.mention}. Bon repos a lui !*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceAft(bot))