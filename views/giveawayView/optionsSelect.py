import discord
from discord.ui import Select
from discord import SelectOption
from functions.functions import *
import asyncio

class optionsGiveawaySelect(Select):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        options = [
            SelectOption(label="Rôle Obligatoire", value="role_obligatoire", description="Définir un rôle obligatoire", emoji="✅"),
            SelectOption(label="Rôle Interdit", value="role_interdit", description="Définir un rôle interdit", emoji="❌"),
            SelectOption(label="Niveau requis", value="niveau_requis", description="Définir un niveau requis", emoji="⬆️"),
            SelectOption(label="Invitations requises", value="invitations_requises", description="Définir un nombre d'invitations", emoji="📨"),
            SelectOption(label="Gagnants imposés", value="gagnants_imposes", description="Forcer certains gagnants", emoji="🏷️"),
            SelectOption(label="Présence en vocal", value="presence_vocal", description="Activer/désactiver la présence en vocal", emoji="🔊")
        ]
        super().__init__(
            placeholder="Options",
            max_values=1,
            min_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        value = self.values[0]
        
        if value == "presence_vocal":
            # Toggle
            await interaction.response.defer(ephemeral=True)
            self.config["presence_vocal"] = not self.config.get("presence_vocal", False)
            await self._update_embed(interaction)
            await interaction.followup.send(f"Présence en vocal: {'✅ Actif' if self.config['presence_vocal'] else '❌ Inactif'}", ephemeral=True)
        elif value == "role_obligatoire" or value == "role_interdit":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("Mentionnez le rôle.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                if message.role_mentions:
                    self.config[value] = message.role_mentions[0].id
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                else:
                    await interaction.followup.send("Aucun rôle mentionné.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        else:
            from views.giveawayView.optionsModal import optionsGiveawayModal
            await interaction.response.send_modal(optionsGiveawayModal(self.bot, self.userId, self.config, value))
    
    async def _update_embed(self, interaction):
        from views.giveawayView.updateHelper import update_giveaway_embed
        await update_giveaway_embed(self.bot, self.userId, self.config, interaction)

