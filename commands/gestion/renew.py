import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *

class renew(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="renew", description="Supprimé et recrée le channel a l'identique")
    async def renew(self, interaction: discord.Interaction, channel: discord.TextChannel = None) -> None:
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        if channel == None:
            channel: discord.TextChannel = interaction.channel

        category: discord.CategoryChannel = channel.category
        await interaction.response.send_message(f"Le salon {channel.mention} sera supprimé dans 3 secondes.", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()
        newChannel: discord.TextChannel = await category.create_text_channel(
            name=channel.name,
            position=channel.position,
            overwrites=channel.overwrites,
            nsfw=channel.nsfw,
            slowmode_delay=channel.slowmode_delay
        )
        await newChannel.send(f"Le salon a été renew par `{interaction.user.name}`.")

async def setup(bot: commands.Bot):
    await bot.add_cog(renew(bot))