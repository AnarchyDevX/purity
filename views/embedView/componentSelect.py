from typing import Any
import discord
from discord.ui import Select
from functions.functions import *
import asyncio
from discord import SelectOption

class componentSelect(Select):
    def __init__(self, userId, bot):
        self.bot = bot
        self.userId = userId
        options = [
            SelectOption(label="Titre", value="title", description="Modifier le titre de l'embed", emoji="🔎"),
            SelectOption(label="Description", value="description", description="Modifier la description de l'embed", emoji="📜"),
            SelectOption(label="Footer (text)", value="footer-text", description="Modifier le footer de l'embed", emoji="🛠️"),
            SelectOption(label="Footer (icon)", value="footer-url", description="Modifier l'icon du footer de l'embed", emoji="⚙️"),
            SelectOption(label="Auteur (text)", value="author-text", description="Modifier l'auteur de l'embed", emoji="✨"),
            SelectOption(label="Auteur (icon)", value="author-url", description="Modifier l'icon de l'auteur de l'embed", emoji="🪄"),
            SelectOption(label="Image", value="image", description="Modifier l'image de l'embed", emoji="📸"),
            SelectOption(label="Add Field", value="add-field", description="Ajouter un field a l'embed", emoji="➕")
        ]
        super().__init__(
            placeholder="Choisissez un élement a modifier",
            max_values=1,
            min_values=1,
            options=options
        )

    async def handler_interaction(self, interaction: discord.Interaction, element: str, maxChar: int, value: str):
        def check(m):
            return m.author == interaction.user and isinstance(m.channel, discord.TextChannel)
        
        await interaction.response.send_message(f"***{element}** doit faire maximum {maxChar} caractères.*", ephemeral=True)
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            newElement = msg.content
            
            if len(newElement) > maxChar:
                await interaction.followup.send(f"*L'élement **{element.lower()}** dépasse la limite de {maxChar} caractères. Veuillez essayer à nouveau.*", ephemeral=True)
                await msg.delete()
                return

            if 'url' in value:
                if newElement.startswith('https://'): 
                    pass
                else:
                    return await interaction.followup.send("Vous devez envoyer un lien valide.", ephemeral=True)
            
            embed = interaction.message.embeds[0]
            if value == "title":
                embed.title = newElement
            elif value == "description":
                embed.description = newElement
            elif value == "footer-text":
                embed.set_footer(text=newElement, icon_url=interaction.message.embeds[0].footer.icon_url)
            elif value == "author-text":
                embed.set_author(name=newElement, icon_url=interaction.message.embeds[0].author.icon_url)
            elif value == "footer-url":
                embed.set_footer(text=interaction.message.embeds[0].footer.text, icon_url=newElement)
            elif value == "author-url":
                embed.set_author(name=interaction.message.embeds[0].author.name, icon_url=newElement)
            if value == "image-url":
                embed.set_image(url=newElement)
            if value == "add-field":
                await interaction.followup.send("***Description du field**, doit faire maximum 4000 caractères.*", ephemeral=True)
                secondMsg = await self.bot.wait_for(f"message", check=check, timeout=60.0)
                fieldValue = secondMsg.content
                if len(fieldValue) > 4000:
                    await interaction.followup.send(f"*Le contenu du field dépasse la limite de 4000 caractères. Veuillez essayer à nouveau.*", ephemeral=True)
                    await msg.delete()
                    await secondMsg.delete()
                    return

                await interaction.followup.send("**Retour a la ligne (oui / non) ?**", ephemeral=True)
                thirdMsg = await self.bot.wait_for('message', check=check, timeout=60.0)
                thirdContent = thirdMsg.content
                inline = None
                if thirdContent == "oui":
                    inline = False
                else:
                    inline = True
                embed.add_field(name=newElement, value=fieldValue, inline=inline)
                await secondMsg.delete()
                await thirdMsg.delete()
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed)
            await msg.delete()

        except asyncio.TimeoutError:
            await interaction.followup.send("Délai dépassé. Modification annulée.", ephemeral=True)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await logs("select embed edit", 3, interaction)
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        match self.values[0]:
            case 'title':
                await self.handler_interaction(
                    interaction,
                    "Titre",
                    maxChar=256,
                    value="title"
                )
            case 'description':
                await self.handler_interaction(
                    interaction,
                    "Description",
                    maxChar=4000,
                    value="description"
                )
            case 'footer-text':
                await self.handler_interaction(
                    interaction,
                    "Footer",
                    maxChar=256,
                    value="footer-text"
                )
            case 'footer-url':
                await self.handler_interaction(
                    interaction,
                    'Footer Url',
                    maxChar=4000,
                    value="footer-url"
                )
            case 'author-text':
                await self.handler_interaction(
                    interaction,
                    "Author",
                    maxChar=256,
                    value="author-text"
                )
            case 'author-url':
                await self.handler_interaction(
                    interaction,
                    "Author Url",
                    maxChar=256,
                    value="author-url"
                )
            case 'image':
                await self.handler_interaction(
                    interaction,
                    'Image',
                    maxChar=4000,
                    value='image-url'
                )
            case 'add-field':
                await self.handler_interaction(
                    interaction,
                    "Titre du field",
                    maxChar=256,
                    value="add-field"
                )