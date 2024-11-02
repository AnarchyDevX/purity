import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class derank(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="derank", description="Retirer tout les roles d'un membre")
    async def derank(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        check: bool =  await check_perms(interaction, 2)
        if check == False:
            return
        
        removedRoles: list[str] = []
        for roles in member.roles:
            try:
                removedRoles.append(roles.mention)
                await member.remove_roles(roles)
            except Exception as e:
                await logs(e, 4, interaction)

        embed: embedBuilder = embedBuilder(
            title="`🛠️`・Derank",
            description=f"*J'ai retirer le maximum de roles à {member.mention}.*",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🪄`・Roles retirés": (
                    "".join(removedRoles),
                    False
                )
            }
        )
        
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(derank(bot))
