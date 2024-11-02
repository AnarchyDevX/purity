import json
import discord
from typing import Dict
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class autoRoleRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="autorole-remove", description="Ajouter un role a l'arrivée")
    async def autoRoleRemove(self, interaction: discord.Interaction, role: discord.Role):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON: Dict[str, any] = load_json_file(f"./configs/{interaction.guild.id}.json")

        roleList: list[int] = guildJSON['configuration']['autorole']
        
        if role.id not in roleList:
            return await err_embed(
                interaction,
                title="Role non configurer",
                description=f"Le role {role.mention} n'est pas présent dans la liste des rôles ajoutés a l'arrivée"
            )        
        
        roleList.remove(role.id)
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed: embedBuilder = embedBuilder(
            title="`🚬`・Rôle retiré",
            description=f"*Le role {role.mention} ne sera désormais plus ajouté dès qu'un membre rejoindra le serveur*",
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoRoleRemove(bot))