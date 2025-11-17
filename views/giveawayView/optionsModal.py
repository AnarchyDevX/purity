import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class optionsGiveawayModal(Modal):
    def __init__(self, bot, userId, config, option_type):
        self.bot = bot
        self.userId = userId
        self.config = config
        self.option_type = option_type
        super().__init__(title="Configuration")
        
        labels = {
            "niveau_requis": "Niveau requis",
            "invitations_requises": "Nombre d'invitations",
            "gagnants_imposes": "IDs des gagnants (séparés par des virgules)"
        }
        
        self.add_item(
            TextInput(
                label=labels.get(option_type, "Valeur"),
                placeholder="Entrez la valeur",
                max_length=100,
                required=True
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        value = self.children[0].value
        
        # Parser selon le type
        try:
            if self.option_type in ["niveau_requis", "invitations_requises"]:
                try:
                    self.config[self.option_type] = int(value)
                except ValueError:
                    return await interaction.followup.send("La valeur doit être un nombre.", ephemeral=True)
            elif self.option_type == "gagnants_imposes":
                # Liste d'IDs séparés par des virgules
                ids = [int(x.strip()) for x in value.split(",") if x.strip().isdigit()]
                self.config[self.option_type] = ids if ids else None
            else:
                self.config[self.option_type] = value
            
            from views.giveawayView.updateHelper import update_giveaway_embed
            await update_giveaway_embed(self.bot, self.userId, self.config, interaction)
        except Exception as e:
            await interaction.followup.send(f"Erreur: {str(e)}", ephemeral=True)

