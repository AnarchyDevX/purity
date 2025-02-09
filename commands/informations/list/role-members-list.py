import discord
from typing import Literal, List
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.rolesMemberListView.suivantButton import suivantButton
from views.rolesMemberListView.precendentButton import precedentButton

class roleMemberList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="all-roles-members", description="Afficher tout les membres ayant un role précis")
    async def roleMemberList(self, interaction: discord.Interaction, role: discord.Role):
        check: bool = await check_perms(interaction, 1)
        if not check:
            return
        
        rolesMemberListed: list[str] = [f'{member.mention} `{member.id}`' for member in interaction.guild.members if role in member.roles]
        
        pages = [rolesMemberListed[i:i + 50] for i in range(0, len(rolesMemberListed), 50)]

        embed: embedBuilder = embedBuilder(
                title=f"`✨`・Liste des membres ayant le role {role.name}",
                description="\n".join(pages[0]),
                color=embed_color(),
                footer=f"Page: {0 + 1}/{len(pages)}"
            )
        
        view = discord.ui.View(timeout=None)
        view.add_item(precedentButton(0, pages))
        view.add_item(suivantButton(0, pages))
        await interaction.response.send_message(embed=embed, view=view)
        

async def setup(bot):
    await bot.add_cog(roleMemberList(bot))