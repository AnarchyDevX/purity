import discord
from discord.ui import Button, View
from functions.functions import *
from views.tempVoc.addModal import addModalTempVoice

class addButtonTempVoice(Button):
    def __init__(self, userId, bot):
        self.userId = userId
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Ajouter",
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        return await interaction.response.send_modal(addModalTempVoice(self.userId, self.bot))