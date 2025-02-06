import asyncio
import discord
from discord.ui import Button
from functions.functions import *

class deleteTempVoice(Button):
    def __init__(self, userId, channel):
        self.userId = userId
        self.channel: discord.VoiceChannel = channel
        super().__init__(
            style=discord.ButtonStyle.grey,
            label="Supprimer",
            emoji="🗑️"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        await interaction.response.send_message("Le salon va être supprimé dans 3 secondes.", ephemeral=True)
        await asyncio.sleep(3)
        await self.channel.delete()
