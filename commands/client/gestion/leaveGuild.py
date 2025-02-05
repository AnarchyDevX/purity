import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class leaveGuild(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="serveur-leave", description="Quitté un serveur")
    async def guildleave(self, interaction: discord.Interaction, guild: str):
        check: bool = await check_perms(interaction, 3)
        if check == False:
            return
        
        try:
            guildId: int = int(guild)
        except ValueError:
            return await err_embed(
                interaction,
                title=f"Id du serveur invalide",
                description=f"L'id du serveur que vous avez fourni est invalide."
            ) 
        
        guild: discord.Guild | None = discord.utils.get(self.bot.guilds, id=guildId)
        if not guild:
            return await err_embed(
                interaction,
                title="Serveur inconnu",
                description="L'id du serveur que vous avez fourni est invalide.",
            )
        await interaction.response.send_message("Je vais quitter le serveur, vous receverez la confirmation en message privé", ephemeral=True)

        try:
            await guild.leave()
        except Exception:
            return await err_embed(
                interaction, 
                title="Impossible de quitter le serveur",
                description=f"Je n'ai pas réussi a quitté le serveur **{guild.name}**",
                followup=True
            )
        
        embed: embedBuilder = embedBuilder(
            title="`✅`・Serveur quitté",
            description=f"J'ai bien quitté le serveur **{guild.name}**.",
            color=embed_color(),
            footer=footer()
        )
        await interaction.user.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(leaveGuild(bot))