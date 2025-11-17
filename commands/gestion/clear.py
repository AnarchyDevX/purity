import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class clear(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="clear", description="Supprimé massivement un nombre definit de messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        check: bool = await check_perms(interaction, 1)
        
        if check == False:
            return
        
        if not 1 <= amount <= 99:
            return await err_embed(
                interaction, 
                title="Nombre incorrect",
                description=f"Vous devez fournir un nombre compris entre `1` et `99`."
            )
        
        await interaction.response.send_message(content=f"`{amount}` vont être supprimés dans le salon {interaction.channel.mention}.", ephemeral=True)
        
        try:
            await interaction.channel.purge(limit=amount)
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Impossible de clear le salon",
                description=f"Je n'ai pas réussi à clear le salon {interaction.channel.mention}. Permission manquante.",
                followup=True
            )
        except discord.HTTPException:
            return await err_embed(
                interaction,
                title="Impossible de clear le salon",
                description=f"Je n'ai pas réussi à clear le salon {interaction.channel.mention}. Erreur Discord API.",
                followup=True
            )
        
        embed: embedBuilder = embedBuilder(
            title="`🧹`・Salon clear avec succès",
            description=f"*`{amount}` messages ont été supprimés dans le salon {interaction.channel.mention} par {interaction.user.mention  }*",
            color=embed_color(),
            footer=footer()
        )

        await interaction.channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(clear(bot))