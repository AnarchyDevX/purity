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
            return await interaction.response.send_message(f"Le rôle {self.role.mention} a été ajouté avec succès", ephemeral=True)
        except discord.Forbidden:
            return await interaction.response.send_message(f"Je n'ai pas réussi à vous ajouter le rôle {self.role.mention}. Permission manquante.", ephemeral=True)
        except discord.HTTPException:
            return await interaction.response.send_message(f"Je n'ai pas réussi à vous ajouter le rôle {self.role.mention}. Erreur Discord API.", ephemeral=True)
        
    