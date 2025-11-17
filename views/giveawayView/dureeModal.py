import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class dureeGiveawayModal(Modal):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        super().__init__(title="Configuration de la durée")
        
        self.add_item(
            TextInput(
                label="Durée (nombre)",
                placeholder="Exemple: 5",
                max_length=10,
                required=True
            )
        )
        self.add_item(
            TextInput(
                label="Unité (sec/min/hour/day/week)",
                placeholder="day",
                max_length=10,
                required=True
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            duree = int(self.children[0].value)
            unite = self.children[1].value.lower()
            
            if unite not in ["sec", "min", "hour", "day", "week"]:
                return await interaction.followup.send("Unité invalide. Utilisez: sec, min, hour, day, ou week.", ephemeral=True)
            
            self.config["duree"] = duree
            self.config["unite"] = unite
            
            from views.giveawayView.updateHelper import update_giveaway_embed
            await update_giveaway_embed(self.bot, self.userId, self.config, interaction)
        except ValueError:
            await interaction.followup.send("La durée doit être un nombre.", ephemeral=True)

