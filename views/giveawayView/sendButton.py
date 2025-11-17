import discord
from discord.ui import Button
from functions.functions import *
from commands.giveaway.gstart import gstart

class sendGiveawayButton(Button):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Envoyer",
            emoji="✅"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        await interaction.response.defer(ephemeral=True)
        
        # Vérifier les champs requis
        if not self.config.get("gain"):
            return await err_embed(
                interaction,
                title="Configuration incomplète",
                description="Vous devez définir le gain du giveaway.",
                followup=True
            )
        
        if not self.config.get("duree") or not self.config.get("unite"):
            return await err_embed(
                interaction,
                title="Configuration incomplète",
                description="Vous devez définir la durée du giveaway.",
                followup=True
            )
        
        if not self.config.get("salon"):
            return await err_embed(
                interaction,
                title="Configuration incomplète",
                description="Vous devez définir le salon où envoyer le giveaway.",
                followup=True
            )
        
        # Récupérer le cog et lancer le giveaway
        cog = self.bot.get_cog("gstart")
        if cog:
            await cog._launch_giveaway(interaction, self.config)
            await interaction.followup.send("✅ Giveaway lancé !", ephemeral=True)

