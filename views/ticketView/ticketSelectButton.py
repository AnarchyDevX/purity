import discord
from discord.ui import Select, View
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.close import closeButtonTicket


class ticketSelectButton(Select):
    def __init__(self, bot, userId, category, optionsList):
        self.bot = bot
        self.userId = userId
        self.category: discord.CategoryChannel = category
        options = [
            discord.SelectOption(label=element['title'], description=element['description'], emoji=element['emojis'], value=element['title']) for element in optionsList
        ]
        super().__init__(
            max_values=1,
            min_values=1,
            placeholder="Selectionnez une option",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = embedBuilder(
            title="`✨`・Tickets",
            description=f"Un membre du staff va vous prendre en charge, merci de patienter",
            color=embed_color(),
            footer=footer()
        )
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),  
            interaction.user: discord.PermissionOverwrite(view_channel=True), 
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True),
        }

        for role in interaction.guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True)

        channel = await self.category.create_text_channel(
            name=f"{interaction.user.name}-{self.values[0]}",
            overwrites=overwrites
        )
        view = discord.ui.View(timeout=None)
        view.add_item(closeButtonTicket())
        await channel.send(embed=embed, content=interaction.user.mention, view=view)
        await interaction.followup.send(f"Votre ticket a été ouvert {channel.mention}", ephemeral=True)