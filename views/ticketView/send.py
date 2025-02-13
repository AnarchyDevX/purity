import discord
from discord.ui import Button, View
from functions.functions import * 
from views.ticketView.ticketSelectButton import ticketSelectButton

class sendButtonTicket(Button):
    def __init__(self, bot, userId, optionsList, channel, category):
        self.channel = channel
        self.category = category
        self.bot = bot
        self.userId = userId
        self.optionsList = optionsList
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="Envoyer",
            emoji="✅"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        embed = interaction.message.embeds[0]
        for i, fields in enumerate(embed.fields):
            if fields.name == "`🔧`・Options configurées":
                embed.remove_field(i)

        view = discord.ui.View(timeout=None)
        view.add_item(ticketSelectButton(self.bot, self.userId, self.category, self.optionsList))
        await self.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Le panel de ticket a bien été envoyé dans le salon {self.channel.mention}", ephemeral=True)