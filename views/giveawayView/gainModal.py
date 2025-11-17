import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class gainGiveawayModal(Modal):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        super().__init__(title="Configuration du gain")
        
        self.add_item(
            TextInput(
                label="Gain",
                placeholder="Exemple: Nitro x3",
                max_length=256,
                required=True
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.config["gain"] = self.children[0].value
        
        from views.giveawayView.updateHelper import update_giveaway_embed
        await update_giveaway_embed(self.bot, self.userId, self.config, interaction)

