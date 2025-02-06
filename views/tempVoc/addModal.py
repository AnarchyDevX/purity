import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class addModalTempVoice(Modal):
    def __init__(self, userId, bot):
        self.bot = bot
        self.userId = userId
        super().__init__(
            title="Configuration"
        )
        self.add_item(
            TextInput(
                label="Salon de redirection",
                placeholder="Exemple: 1278748685685100556",
                min_length=1,
                max_length=100,
                required=True,
                style=discord.TextStyle.short
            )
        )
        self.add_item(
            TextInput(
                label="Categorie du salon temporaire",
                placeholder="Exemple: 1278774209513914506",
                min_length=1,
                max_length=100,
                required=True,
                style=discord.TextStyle.short
            )
        )

    def get_category_name(self, interaction: discord.Interaction, id: int):
        category: discord.CategoryChannel | None = discord.utils.get(interaction.guild.categories, id=id)
        return category.name

    async def on_submit(self, interaction: discord.Interaction):
        from views.tempVoc.addButton import addButtonTempVoice
        from views.tempVoc.removeButton import removeButtonTempVoice

        channelId = self.children[0].value
        categoryId = self.children[1].value
        try: channelId = int(channelId)
        except Exception: return await err_embed(interaction=interaction, title="Id du channel invalide", description="L'id du salon que vous avez fourni est invalide.")
        try: categoryId = int(categoryId)
        except Exception: return await err_embed(interaction=interaction, title="Id de la categorie invalide", description="L'id de la categorie que vous avez fourni est invalide.")
        channel = interaction.guild.get_channel(channelId)
        category = discord.utils.get(interaction.guild.categories, id=categoryId)
        if not channel: return await err_embed(interaction=interaction, title="Id du channel invalide", description="L'id du salon que vous avez fourni est invalide.")
        if not category: return await err_embed(interaction=interaction, title="Id de la categorie invalide", description="L'id de la categorie que vous avez fourni est invalide.")

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        for element in guildJSON['configuration']['tempvoices']['configs']:
            if int(element) == channel.id:
                return await err_embed(interaction=interaction, title="Salon déjà configurer", description=f"Le salon {channel.mention} est déjà utilisé comme salon pour crée des vocales temporaires")
        payloads: dict[str, int] = {
            "category": category.id
        }
        guildJSON['configuration']['tempvoices']['configs'][str(channel.id)] = payloads
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        tempvoiceConfigs = guildJSON['configuration']['tempvoices']['configs']
        voiceList = [
            f'> `🪄`・**Channel:** <#{element}>\n'
            f"> `🛠️`・**Categorie:** `{self.get_category_name(interaction, item['category'])}`\n"
            for element, item in tempvoiceConfigs.items()
        ]
        embed: embedBuilder = embedBuilder(
            title=f"`🔊`・Liste des salons de creations de vocaux temporaires",
            description="\n".join(voiceList),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(addButtonTempVoice(self.userId, self.bot))
        view.add_item(removeButtonTempVoice(self.userId, self.bot))
        await interaction.response.edit_message(embed=embed, view=view)