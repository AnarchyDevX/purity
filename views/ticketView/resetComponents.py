import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class resetComponentTicket(Button):
    def __init__(self, bot, userId, optionsList, channel, category):
        self.channel = channel
        self.category = category
        self.bot = bot
        self.userId = userId
        self.optionsList = optionsList
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Reset",
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        embed = interaction.message.embeds[0]
        embed.clear_fields()
        self.optionsList = []
        
        from views.ticketView.embedAddSelect import embedAddSelect
        from views.ticketView.addComponent import addComponentTicket
        from views.ticketView.embedResetSelect import embedResetSelect 
        from views.ticketView.send import sendButtonTicket

        view = discord.ui.View(timeout=None)
        view.add_item(embedAddSelect(self.userId, self.bot, self.optionsList, self.channel, self.category))
        view.add_item(embedResetSelect(self.userId, self.bot, self.optionsList, self.channel, self.category))
        view.add_item(addComponentTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))
        view.add_item(resetComponentTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))
        view.add_item(sendButtonTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))

        return await interaction.response.edit_message(embed=embed, view=view)