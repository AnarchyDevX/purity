import discord
from discord.ui import Button
from functions.functions import *

class badwordsRemoveButton(Button):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            label=f"Retirer",
            style=discord.ButtonStyle.red,
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.userId != interaction.user.id:
            return await unauthorized(interaction)
        
        from views.badwords.removeModal import badwordRemoveModal

        await interaction.response.send_modal(badwordRemoveModal(self.userId))
        