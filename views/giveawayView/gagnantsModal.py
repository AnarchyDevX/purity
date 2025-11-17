import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class gagnantsGiveawayModal(Modal):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        super().__init__(title="Nombre de gagnants")
        
        self.add_item(
            TextInput(
                label="Nombre de gagnants",
                placeholder="Exemple: 1",
                max_length=3,
                required=True
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            gagnants = int(self.children[0].value)
            if gagnants < 1:
                return await interaction.followup.send("Le nombre de gagnants doit être supérieur à 0.", ephemeral=True)
            
            self.config["gagnants"] = gagnants
            
            from views.giveawayView.updateHelper import update_giveaway_embed
            await update_giveaway_embed(self.bot, self.userId, self.config, interaction)
        except ValueError:
            await interaction.followup.send("Le nombre de gagnants doit être un nombre.", ephemeral=True)

