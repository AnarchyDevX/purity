import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.embedAddSelect import embedAddSelect
from views.ticketView.embedResetSelect import embedResetSelect
from views.ticketView.addComponent import addComponentTicket
from views.ticketView.resetComponents import resetComponentTicket
from views.ticketView.send import sendButtonTicket

class ticketsConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @app_commands.command(name="ticket-config", description=f"Configurer et envoyer un embed de tickets")
    async def ticketConfig(self, interaction: discord.Interaction, channel: discord.TextChannel, category: discord.CategoryChannel):
        optionsList = []
        if not await check_perms(interaction, 2): return

        embed: embedBuilder = embedBuilder(
            title="Titre",
            description="*Description*",
            color=embed_color()
        )
        view: discord.ui.View = discord.ui.View(timeout=None)
        view.add_item(embedAddSelect(interaction.user.id, self.bot, optionsList, channel, category))
        view.add_item(embedResetSelect(interaction.user.id, self.bot, optionsList, channel, category))
        view.add_item(addComponentTicket(self.bot, interaction.user.id, optionsList, channel, category))
        view.add_item(resetComponentTicket(self.bot, interaction.user.id, optionsList, channel, category))
        view.add_item(sendButtonTicket(self.bot, interaction.user.id, optionsList, channel, category))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ticketsConfig(bot))