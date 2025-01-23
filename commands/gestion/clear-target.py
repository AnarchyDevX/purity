import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class clearTarget(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="clear-target", description="Supprimer les messages d'un utilisateur particulier.")
    async def clearTarget(self, interaction: discord.Interaction, member: discord.Member, number: int, channel: discord.TextChannel = None):
        if not await check_perms(interaction, 2): return
        if channel == None:
            channel = interaction.channel
        await interaction.response.defer(ephemeral=True)

        def is_target_message(msg):
            return msg.author == member
        
        await channel.purge(limit=number * 2, check=is_target_message)

        embed = embedBuilder(
            title="`🪄`・Message clear",
            description=f"*`{number}`* messages de {member.mention} on été supprimés dans le salon {channel.mention}",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(clearTarget(bot))