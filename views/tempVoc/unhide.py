import discord
from discord.ui import Button, View
from functions.functions import *

class unhideTempVoice(Button):
    def __init__(self, userId, channel):
        self.channel: discord.VoiceChannel = channel
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.grey,
            label="Unhide",
            emoji="👁️"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        overwrites = {}
        
        overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(view_channel=True)
        
        await self.channel.edit(overwrites=overwrites)
        await interaction.response.send_message("Le salon n'est plus caché pour les autres utilisateurs.", ephemeral=True)
