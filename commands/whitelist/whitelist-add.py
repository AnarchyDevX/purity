import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class whitelistAdd(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="whitelist-add", description='Ajouter un membre a la whitelist')
    async def whitelistAdd(self, interaction: discord.Interaction, member: discord.Member):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        whitelist = guildJSON['whitelist']

        if member.id in whitelist:
            return await err_embed(
                interaction,
                title="Membre déjà whitelist",
                description=f"Le membre {member.mention} est déjà présent dans la whitelist"
            )
        
        whitelist.append(member.id)
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`⚪`・Whitelist",
            description=f"*Le membre {member.mention} à été ajouté a la whitelist*",
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(whitelistAdd(bot))