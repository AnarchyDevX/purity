import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.tempVoc.addButton import addButtonTempVoice
from views.tempVoc.removeButton import removeButtonTempVoice

class tempVoiceList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    def get_category_name(self, interaction: discord.Interaction, id: int):
        category: discord.CategoryChannel | None = discord.utils.get(interaction.guild.categories, id=id)
        return category.name
    
    @app_commands.command(name="tempvoice-config", description="Configurer les salon vocaux temporaires.")
    async def tempvoiceList(self, interaction: discord.Interaction):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
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
        view.add_item(addButtonTempVoice(interaction.user.id, self.bot))
        view.add_item(removeButtonTempVoice(interaction.user.id, self.bot))
        await interaction.response.send_message(embed=embed, view=view)
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tempVoiceList(bot))