import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class emojiGiveawayModal(Modal):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        super().__init__(title="Configuration de l'émoji")
        
        self.add_item(
            TextInput(
                label="Émoji",
                placeholder="🎉",
                max_length=10,
                required=True
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.config["emoji"] = self.children[0].value
        
        from views.giveawayView.updateHelper import update_giveaway_embed
        await update_giveaway_embed(self.bot, self.userId, self.config, interaction)

