import discord
from discord.ui import Button

class roleReactButton(Button):
    def __init__(self, role):
        self.role: discord.Role = role
        super().__init__(
            style=discord.ButtonStyle.grey,
            emoji="🪄"
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.user.add_roles(self.role)
            return await interaction.response.send_message(f"Le rôle {self.role.mention} as été ajouté avec succès", ephemeral=True)
        except Exception as e:
            return await interaction.response.send_message(f"Je n'ai pas réussi a t'ajouter le rôle {self.role.mention}.", ephemeral=True)
        
    