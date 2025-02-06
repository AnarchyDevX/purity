import discord
from discord.ui import Button
from functions.functions import *
from views.tempVoc.nameModal import nameTempVoiceModal

class nameTempVoice(Button):
    def __init__(self, userId, channel):
        self.channel: discord.VoiceChannel = channel
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="Nom",
            emoji="⚙️"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        return await interaction.response.send_modal(nameTempVoiceModal(self.channel))