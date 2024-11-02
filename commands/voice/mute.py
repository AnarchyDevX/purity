import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class voiceMute(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-mute", description="Rendre muet un membre en vocal.")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="on", value="True"),
            app_commands.Choice(name="off", value="False")
        ]
    )
    async def voiceMute(self, interaction: discord.Interaction, option: str, member: discord.Member) -> None:
        await logs("voice-mute", 1, interaction)
        if option == "True":
            option = True
        else:
            option = False

        check: bool = await check_perms(interaction, 1)
        
        if check == False:
            return
        
        if not member.voice:
            return await err_embed(
                interaction,
                title="Salon manquant",
                description=f"Le membre {member.mention} n'est pas présent dans un salon vocal."
            )
        
        try:
            await member.edit(mute=option)
        except Exception:
            return await err_embed(
                interaction,
                title="Impossible de rendre muet le membre",
                description=f"Je n'ai pas réussi à rendre muet le membre {member.mention}"
            )
        text: None = None
        if option == False:
            text: str = f"*Le membre {member.mention} à bien été demute.*"
        else:
            text: str = f"*Le membre {member.mention} à bien été mute.*"

        embed: embedBuilder = embedBuilder(
            title="`✅`・Mute vocal",
            description=text,
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceMute(bot))