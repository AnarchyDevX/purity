import discord
from discord.ui import Button, View
from functions.functions import *

class hideTempVoice(Button):
    def __init__(self, userId, channel):
        self.channel: discord.VoiceChannel = channel
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.grey,
            label="Hide",
            emoji="🙈"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        overwrites = {}
        for member in self.channel.members:
            overwrites[member] = discord.PermissionOverwrite(view_channel=True)
        
        overwrites[interaction.guild.default_role] = discord.PermissionOverwrite(view_channel=False)
        
        await self.channel.edit(overwrites=overwrites)
        await interaction.response.send_message("Salon caché pour les autres utilisateurs.", ephemeral=True)
