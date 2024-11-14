import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class lockChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="channel-lock", description="Verrouiller un salon textuel")
    async def channelLock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if not await check_perms(interaction, 2): return
        if channel == None:
            channel = interaction.channel

        await interaction.response.defer()
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        for role in channel.overwrites:
            try: await channel.set_permissions(role, send_messages=False)
            except Exception: continue
        
        embed = embedBuilder(
            title="`🔐`・Lock", 
            description=f"*Le salon {channel.mention} à été lock.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(lockChannel(bot))