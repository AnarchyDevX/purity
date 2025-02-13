import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.addModal import addModalTicket

class addComponentTicket(Button):
    def __init__(self, bot, userId, optionsList, channel, category):
        self.channel = channel
        self.category = category
        self.bot = bot
        self.userId = userId
        self.optionsList = optionsList
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Ajouter une option",
            emoji="➕"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        return await interaction.response.send_modal(addModalTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))