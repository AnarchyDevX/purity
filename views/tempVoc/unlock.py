import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class unlockTempVoice(Button):
    def __init__(self, userId, channel):
        self.userId = userId
        self.channel: discord.VoiceChannel = channel
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="Unlock",
            emoji="🔓"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        await self.channel.edit(user_limit=None)
        await interaction.response.send_message("Le salon vocal à été unlock", ephemeral=True)