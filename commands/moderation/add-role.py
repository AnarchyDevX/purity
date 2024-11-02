import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class addRole(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="role-add", description="Ajouter un role a un membre")
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role) -> None:
        await logs("role-add", 1, interaction)
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        try:
            await member.add_roles(role)
        except Exception as e:
            await logs(e, 4, interaction)
            return await err_embed(
                interaction,
                title="Erreur lors de l'ajout du rôle",
                description=f"*Je n'ai pas réussi à ajouter le role {role.mention} à {member.mention}*"
            )
        embed: embedBuilder = embedBuilder(
            title="`✅`・Role ajouté avec succès",
            description=f"*Le membre {member.mention} à bien reçu le rôle {role.mention}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(addRole(bot))