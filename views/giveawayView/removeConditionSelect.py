import discord
from discord.ui import Select
from functions.functions import *

class removeConditionSelect(Select):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        
        options = []
        for i, condition in enumerate(config.get("conditions_custom", [])):
            display_text = condition[:50] + "..." if len(condition) > 50 else condition
            options.append(discord.SelectOption(
                label=f"Condition {i+1}",
                description=display_text,
                value=str(i)
            ))
        
        super().__init__(
            placeholder="Sélectionnez une condition à supprimer",
            max_values=1,
            min_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        index = int(self.values[0])
        conditions = self.config.get("conditions_custom", [])
        
        if 0 <= index < len(conditions):
            removed = conditions.pop(index)
            self.config["conditions_custom"] = conditions
            await self._update_embed(interaction)
            await interaction.followup.send(f"✅ Condition supprimée: *{removed[:100]}...*", ephemeral=True)
        else:
            await interaction.followup.send("❌ Index invalide.", ephemeral=True)
    
    async def _update_embed(self, interaction):
        from views.giveawayView.updateHelper import update_giveaway_embed
        await update_giveaway_embed(self.bot, self.userId, self.config, interaction)

