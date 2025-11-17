import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class jail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="jail", description=f"Envoyé un membre en prison")
    async def jail(self, interaction: discord.Interaction, member: discord.Member):
        if not await check_perms(interaction, 2): return
        await interaction.response.defer()
        removedRoles: list[str] = []
        for roles in member.roles:
            try:
                removedRoles.append(roles.mention)
                await member.remove_roles(roles)
            except discord.Forbidden:
                # Bot n'a pas les permissions
                await logs(f"Impossible de retirer le rôle {roles.name} (Forbidden)", 4, interaction)
            except discord.HTTPException:
                # Erreur Discord API
                await logs(f"Erreur lors de la suppression du rôle {roles.name} (HTTPException)", 4, interaction)
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        roleId = guildJSON['jail']['role']
        role = discord.utils.get(interaction.guild.roles, id=roleId)
        if role:
            await member.add_roles(role)
        else:
            return await err_embed(
                interaction,
                title=f"Impossible d'ajouter le role",
                description=f"Je n'ai pas réussi a ajouté le role {role.mention} a {member}.",
                followup=True
            )
        embed = embedBuilder(
            title=f"`🔨`・Jail",
            description=f"*Le membre {member.mention} à bien été envoyé en prison.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(jail(bot))