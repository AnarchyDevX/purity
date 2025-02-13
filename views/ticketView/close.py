import asyncio
import discord
from discord.ext import commands
from discord.ui import Button


class closeButtonTicket(Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Close",
            emoji="🔒"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Le ticket a été fermer. Ce salon sera supprimé dans 5 secondes")
        await asyncio.sleep(5)
        await interaction.channel.delete()