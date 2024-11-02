from typing import Any
import discord
from functions.functions import *
from discord.ui import Button
from .channelModal import channelModal

class sendButton(Button):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Envoyer",
            emoji="✅"
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        await logs("button embed send", 3, interaction)
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        await interaction.response.send_modal(channelModal())
