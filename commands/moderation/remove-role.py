import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class removeRole(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="role-remove", description="Ajouter un role a un membre")
    async def removerole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role) -> None:
        await logs("role-remove", 1, interaction)
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        if role not in member.roles:
            return await err_embed(
                interaction,
                title="Le membre ne possède pas le rôle",
                description=f"Le membre {member.mention} ne possède pas le rôle {role.mention}"
            )
        
        try:
            await member.remove_roles(role)
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Impossible de retirer le role",
                description=f"Je n'ai pas réussi à retirer le role {role.mention} à {member.mention}. Permission manquante."
            )
        except discord.HTTPException:
            return await err_embed(
                interaction,
                title="Impossible de retirer le role",
                description=f"Je n'ai pas réussi à retirer le role {role.mention} à {member.mention}. Erreur Discord API."
            )
        
        embed: embedBuilder = embedBuilder(
            title="`✅`・Role retiré avec succès",
            description=f"*Le rôle {role.mention} à bien été retiere à {member.mention}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(removeRole(bot))