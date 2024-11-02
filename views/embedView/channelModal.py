import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class channelModal(Modal):
    def __init__(self) -> None:
        super().__init__(
            title="Envoyer l'embed"
        )

        channelId = TextInput(
            label="Id du salon:",
            placeholder="Exemple: 1299371313164451851",
            min_length=1,
            required=True
        )

        self.add_item(channelId)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await logs('modal embed send', 3, interaction)
        channelId = self.children[0].value
        try:
            channelId = int(channelId)
        except ValueError:
            embed = discord.Embed(
                title="`❌`・Channel Id invalide",
                description="*L'id que vous avez fourni n'est pas valide.*",
                color=embed_color()
            )
            embed.set_footer(text=footer())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        channel = discord.utils.get(interaction.guild.channels, id=channelId)
        if channelId == None:
            embed = discord.Embed(
                title="`❌`・Channel Id invalide",
                description="*L'id que vous avez fourni n'est pas celui d'un channel valide.*",
                color=embed_color()
            )
            embed.set_footer(text=footer())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        embed = discord.Embed(
            title="`✅`・Embed envoyé avec succès",
            description=f"*L'embed que vous venez de configurer à été envoyé avec succès dans la salon {channel.mention}.*",
            color=embed_color()
        )
        embed.set_footer(text=footer())
        await channel.send(embed=interaction.message.embeds[0], view=None, content=None)
        await interaction.response.send_message(f"L'embed a bien été envoyé dans le salon {channel.mention}", ephemeral=True)
        await interaction.message.delete()