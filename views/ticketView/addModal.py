import discord
from discord.ui import Modal, View, TextInput
from functions.functions import *
from core.embedBuilder import embedBuilder

class addModalTicket(Modal):
    def __init__(self, bot, userId, optionsList, channel, category):
        self.channel = channel
        self.category = category
        self.bot = bot
        self.userId = userId
        self.optionsList: list = optionsList
        super().__init__(
            title="Ajout d'une option"
        )
        self.add_item(
            TextInput(
                label="Nom de l'options",
                max_length=21,
                min_length=1,
                required=True
            )
        )
        self.add_item(
            TextInput(
                label="Description de l'option",
                max_length=100,
                min_length=1,
                required=True
            )
        )
        self.add_item(
            TextInput(
                label="Emojis",
                max_length=100,
                min_length=1,
                required=True
            )
        )

    async def on_submit(self, interaction: discord.Interaction):
        payload = {
            "title": self.children[0].value,
            "description": self.children[1].value,
            "emojis": self.children[2].value
        }
        self.optionsList.append(payload)

        embed = interaction.message.embeds[0]
        embed.clear_fields()
        embed.add_field(
            name="`🔧`・Options configurées",
            value=f"```" + '\n\n'.join(f"Nom: {element['title']}\nDescription: {element['description']}\nEmojis: {element['emojis']}" for element in self.optionsList) +"```",
            inline=False
        )

        from views.ticketView.addComponent import addComponentTicket
        from views.ticketView.embedResetSelect import embedResetSelect 
        from views.ticketView.resetComponents import resetComponentTicket
        from views.ticketView.embedAddSelect import embedAddSelect
        from views.ticketView.send import sendButtonTicket

        view = discord.ui.View(timeout=None)
        view.add_item(embedAddSelect(self.userId, self.bot, self.optionsList, self.channel, self.category))
        view.add_item(embedResetSelect(self.userId, self.bot, self.optionsList, self.channel, self.category))
        view.add_item(addComponentTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))
        view.add_item(resetComponentTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))
        view.add_item(sendButtonTicket(self.bot, self.userId, self.optionsList, self.channel, self.category))

        return await interaction.response.edit_message(embed=embed, view=view)