import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class whitelistRemove(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="whitelist-remove", description='Retirer un membre de la whitelist')
    async def whitelistRemove(self, interaction: discord.Interaction, member: str):
        if not await check_perms(interaction, 2):
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
        whitelist = guildJSON['whitelist']

        if member not in whitelist:
            return await err_embed(
                interaction,
                title="Membre non whitelist",
                description=f"Le membre {member.mention} n'est pas présent dans la whitelist"
            )
        
        whitelist.remove(member)
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed = embedBuilder(
            title="`⚪`・Whitelist",
            description=f"*Le membre avec l'id `{member}` à été retiré de la whitelist*",
            footer=footer(),
            color=embed_color()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(whitelistRemove(bot))