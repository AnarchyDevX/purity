import discord
from discord.ui import Button
from functions.functions import *

class badwordsAddButton(Button):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            label=f"Ajouter",
            style=discord.ButtonStyle.green,
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.userId != interaction.user.id:
            return await unauthorized(interaction)
        
        from views.badwords.addModal import badwordAddModal

        await interaction.response.send_modal(badwordAddModal(self.userId))