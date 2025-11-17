import discord
from functions.functions import *
from discord.ext import commands
from discord import app_commands
from core.embedBuilder import embedBuilder

class voiceDeaf(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="voice-deaf", description="Mettre en sourdine un membre en vocal.")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="on", value="True"),
            app_commands.Choice(name="off", value="False")
        ]
    )
    async def voiceDeaf(self, interaction: discord.Interaction, option: str, member: discord.Member) -> None:
        await logs("voice-deaf", 1, interaction)
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
                title="Salon introuvable",
                description=f"Le membre {member.mention} n'est pas présent dans un salon vocal."
            )
        
        try:
            await member.edit(deafen=option)
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Impossible de mettre en sourdine le membre",
                description=f"Je n'ai pas réussi à mettre en sourdine le membre {member.mention}. Permission manquante."
            )
        except discord.HTTPException:
            return await err_embed(
                interaction,
                title="Impossible de mettre en sourdine le membre",
                description=f"Je n'ai pas réussi à mettre en sourdine le membre {member.mention}. Erreur Discord API."
            )
        
        text: None = None
        if option == False:
            text: str = f"*Le membre {member.mention} à bien été mis en sourdine.*"
        else:
            text: str = f"*Le membre {member.mention} à bien été mis en sourdine.*"

        embed: embedBuilder = embedBuilder(
            title="`✅`・Mise en sourdine vocal",
            description=text,
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(voiceDeaf(bot))