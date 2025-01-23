import asyncio
import discord
from discord.ext import commands
from discord.ui import Button
from functions.functions import *

class autoroleRemoveButton(Button):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            label="Retirer",
            style=discord.ButtonStyle.red,
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.autoRole.removeModal import autoRoleRemoveModal

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        await interaction.response.send_modal(autoRoleRemoveModal(self.userId, self.bot))
