import discord
from discord.ui import Modal

class nameTempVoiceModal(Modal):
    def __init__(self, channel):
        self.channel: discord.VoiceChannel = channel
        super().__init__(title="Nom du salon")
        self.add_item(
            discord.ui.TextInput(
                label="Changement de nom",
                style=discord.TextStyle.short,
                max_length=25,
                min_length=1,
                required=True,
                placeholder="Entrez le nouveau nom du salon..."
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await self.channel.edit(name=self.children[0].value)
        return await interaction.response.send_message("Le nom du salon a été modifié avec succès.", ephemeral=True)

