import discord
import aiohttp
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class changeClientBanner(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="banner-edit", description="Changer la banniere du bot")
    async def botEditBanner(self, interaction: discord.Interaction, url :str):
        check: bool = await check_perms(interaction, 3)
        if check == False:
            return
        
        if not url.startswith("https://"):
            return await err_embed(
                interaction,
                title="Lien invalide",
                description="Le lien que vous avez fourni est invalide."
            )
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status != 200:
                    return await err_embed(
                        interaction, 
                        title="Impossible de récuperer l'image",
                        description="Je n'ai pas réussi a lire et récuperer votre image",
                        followup=True
                    )
                newBanner = await r.read()
                
        try:
            await self.bot.user.edit(banner=newBanner)
        except Exception as e:
            return await err_embed(
                interaction,
                title="Erreur lors du changement",
                description="Une erreur est survenu lors du changement de la banniere du bot",
                followup=True
            )
        
        embed = embedBuilder(
            title="`🪄`・Banniere Changé",
            description="*La banniere du bot a bien été modifiée*",
            color=embed_color(),
            footer=footer()
        ) 
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(changeClientBanner(bot))