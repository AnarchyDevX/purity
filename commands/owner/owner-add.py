import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class ownerAdd(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="owner-add", description='Ajouter un membre a la list des owner')
    async def ownerAdd(self, interaction: discord.Interaction, member: discord.Member):
        if not await check_perms(interaction, 3):
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        owner = guildJSON['ownerlist']

        if member.id in owner:
            return await err_embed(
                interaction,
                title="Membre déjà owner",
                description=f"Le membre {member.mention} est déjà présent dans la list des owner"
            )
        
        owner.append(member.id)
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`⚪`・Owner",
            description=f"*Le membre {member.mention} à été ajouté a la liste des owner*",
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ownerAdd(bot))