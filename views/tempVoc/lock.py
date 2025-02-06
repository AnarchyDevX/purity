import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class lockTempVoice(Button):
    def __init__(self, userId, channel):
        self.userId = userId
        self.channel: discord.VoiceChannel = channel
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="Lock",
            emoji="🔐"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        await self.channel.edit(user_limit=len(self.channel.members))
        await interaction.response.send_message("Le salon vocal à été lock", ephemeral=True)
        

