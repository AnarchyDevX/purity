import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class ownerRemove(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="owner-remove", description='Retirer un membre de la liste des owner')
    async def ownerRemove(self, interaction: discord.Interaction, member: str):
        if not await check_perms(interaction, 3):
            return
        
        try: 
            member = int(member)
        except ValueError:
            return await err_embed(
                interaction,
                title="Id invalide",
                description=f"L'id que vous avez fourni est invalide"
            )
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        owner = guildJSON['ownerlist']

        if member not in owner:
            return await err_embed(
                interaction,
                title="Membre non owner",
                description=f"Le membre {member.mention} n'est pas présent dans la list des owner"
            )
        
        owner.remove(member)
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`⚪`・Owner",
            description=f"*Le membre avec l'id `{member}` à été retiré de la liste des owner*",
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ownerRemove(bot))