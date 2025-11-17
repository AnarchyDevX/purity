import asyncio
import discord 
from discord.ui import Button
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class removeButtonTempVoice(Button):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Supprimer",
            emoji="➖"
        )


    def get_category_name(self, interaction: discord.Interaction, id: int):
        category: discord.CategoryChannel | None = discord.utils.get(interaction.guild.categories, id=id)
        return category.name


    async def callback(self, interaction: discord.Interaction):
        from views.tempVoc.addButton import addButtonTempVoice

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        try:
            await interaction.response.send_message("Veuillez mentionner le salon que vous voulez supprimer des configurations", ephemeral=True)
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            channel = message.channel_mentions[0]
            for element in guildJSON['configuration']['tempvoices']['configs']:
                if int(element) == channel.id:
                    del guildJSON['configuration']['tempvoices']['configs'][str(channel.id)]
                    with open(f'./configs/{interaction.guild.id}.json', 'w', encoding='utf-8') as f:
                        json.dump(guildJSON, f, indent=4)
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
                    await message.delete()
                    return await interaction.followup.edit_message(embed=embed, view=view, message_id=interaction.message.id)
                
            await err_embed(
                interaction, 
                title="Salon non configuré",
                description=f"Le salon {channel.mention} n'est pas présent dans la liste des salons de créations de vocales temporaires", 
                followup=True
            )
            return await message.delete()
        except asyncio.TimeoutError:
            return await interaction.followup.send("Delai ecouler", ephemeral=True)
