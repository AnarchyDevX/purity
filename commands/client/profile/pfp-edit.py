import discord
import aiohttp
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class changeClientPfp(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="pfp-edit", description="Modifier la photo de profil du bot")
    async def botEditGuildPfp(self, interaction: discord.Interaction, url: str):
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
                newPfp = await r.read()
                
        try:
            await self.bot.user.edit(avatar=newPfp)
        except Exception as e:
            return await err_embed(
                interaction,
                title="Erreur lors du changement",
                description="Une erreur est survenu lors du changement de l'avatar du bot",
                followup=True
            )
        
        embed = embedBuilder(
            title="`🪄`・Avatar Changé",
            description="*L'avatar du bot a bien été modifier*",
            color=embed_color(),
            footer=footer()
        ) 
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(changeClientPfp(bot))