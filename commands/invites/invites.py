import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class invitesStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invites", description="Afficher le nombre d'invitation effectuer par un membre")
    async def invites(self, interaction: discord.Interaction, member: discord.Member = None):
        userInvites = 0
        if not member: member = interaction.user
        for invite in await interaction.guild.invites():
            if invite.inviter == interaction.user:
                userInvites += invite.uses

        return await interaction.response.send_message(content=userInvites)                    
        

async def setup(bot):
    await bot.add_cog(invitesStats(bot))


