import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *

class mp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mp", description="Envoyer un message privé a un membre")
    async def mp(self, interaction: discord.Interaction, member: discord.Member, message: str):
        check = await check_perms(interaction, 1)
        if check == False:
            return
        
        await interaction.response.defer(ephemeral=True)
        try:
            await member.send(content=message)
        except discord.Forbidden:
            # L'utilisateur a désactivé les DMs
            return await err_embed(
                interaction, 
                title="Impossible d'envoyer le message",
                description=f"Je n'ai pas réussi à envoyer le message à {member.mention}. Les messages privés sont peut-être désactivés.",
                followup=True
            )
        except discord.HTTPException:
            return await err_embed(
                interaction, 
                title="Impossible d'envoyer le message",
                description=f"Je n'ai pas réussi à envoyer le message à {member.mention}. Erreur Discord API.",
                followup=True
            )

        await interaction.followup.send(content=f"Le message à été envoyer en message privée a {member.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(mp(bot))