from typing import Any
import discord
from discord.ui import Select
from functions.functions import *
from discord import SelectOption

class componentResetSelect(Select):
    def __init__(self, userId, bot):
        self.bot = bot
        self.userId = userId
        options = [
            SelectOption(label="Titre", value="title", description="Réinitialiser le titre de l'embed", emoji="🔎"),
            SelectOption(label="Description", value="description", description="Réinitialiser la description de l'embed", emoji="📜"),
            SelectOption(label="Footer (text)", value="footer-text", description="Réinitialiser le footer de l'embed", emoji="🛠️"),
            SelectOption(label="Footer (icon)", value="footer-url", description="Réinitialiser l'icon du footer de l'embed", emoji="⚙️"),
            SelectOption(label="Auteur (text)", value="author-text", description="Réinitialiser l'auteur de l'embed", emoji="✨"),
            SelectOption(label="Auteur (icon)", value="author-url", description="Réinitialiser l'icon de l'auteur de l'embed", emoji="🪄"),
            SelectOption(label="Image", value="image", description="Réinitialiser l'image de l'embed", emoji="📸"),
            SelectOption(label="Fields", value="fields", description="Réinitialiser les fields de l'embed", emoji="➕"),
            SelectOption(label="Lien", value="link", description="Réinitialiser le lien de l'embed", emoji="🔗")
        ]
        super().__init__(
            placeholder="Choisissez un élement a réinitialiser",
            max_values=1,
            min_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        await logs("select embed reset", 3, interaction)
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        match self.values[0]:
            case 'title':
                embed = interaction.message.embeds[0]
                embed.title = "Titre"
                await interaction.response.edit_message(embed=embed)
            case 'description':
                embed = interaction.message.embeds[0]
                embed.description = "Description"
                await interaction.response.edit_message(embed=embed)
            case 'footer-text':
                embed = interaction.message.embeds[0]
                embed.set_footer(text=None, icon_url=interaction.message.embeds[0].footer.icon_url)
                await interaction.response.edit_message(embed=embed)
            case 'footer-icon':
                embed = interaction.message.embeds[0]
                embed.set_footer(text=interaction.message.embeds[0].footer.text, icon_url=None)
                await interaction.response.edit_message(embed=embed)
            case 'author-text':
                embed = interaction.message.embeds[0]
                embed.set_author(name=None, icon_url=interaction.message.embeds[0].author.icon_url)
                await interaction.response.edit_message(embed=embed)
            case 'author-url':
                embed = interaction.message.embeds[0]
                embed.set_footer(text=interaction.message.embeds[0].author.name, icon_url=None)
                await interaction.response.edit_message(embed=embed)
            case 'image':
                embed = interaction.message.embeds[0]
                embed.set_image(url=None)
                await interaction.response.edit_message(embed=embed)
            case 'fields':
                embed = interaction.message.embeds[0]
                for i in range(len(embed.fields)):
                    embed.remove_field(i)
                await interaction.response.edit_message(embed=embed)
            case 'link':
                embed = interaction.message.embeds[0]
                embed.url = ""
                await interaction.response.edit_message(embed=embed)