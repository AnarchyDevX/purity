import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class changeServerName(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="name-edit", description="Changer le nom du bot uniquement sur le serveur")
    async def botEditGuildName(self, interaction: discord.Interaction, name: str):
        oldName = self.bot.user.name
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        await interaction.response.defer()
        try:
            await interaction.guild.me.edit(nick=name)
        except Exception as e:
            return await err_embed(
                interaction, 
                title="Impossible de changer le nom",
                description="Je n'ai pas réussi a changer mon nom sur le serveur", 
                followup=False
            )
        
        embed: embedBuilder = embedBuilder(
            title="`📀`・Nom du bot changé",
            description=f"*Le nom du bot a été modifier*",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🔨`・Ancien Nom": (
                    f"> `{oldName}`",
                    True
                ),
                "`🛠️`・Nouveau Nom": (
                    f"> `{name}`",
                    True
                )
            }
        )
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(changeServerName(bot))