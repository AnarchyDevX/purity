import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class RejectSuspicionButton(Button):
    def __init__(self, word: str):
        self.word = word
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Rejeter",
            emoji="❌"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Erreur",
                description="Configuration introuvable."
            )
        
        # Supprimer la suspicion
        if 'badwords_learning' in guildJSON and 'suspicions' in guildJSON['badwords_learning']:
            if self.word in guildJSON['badwords_learning']['suspicions']:
                del guildJSON['badwords_learning']['suspicions'][self.word]
        
        # Sauvegarder
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        embed = embedBuilder(
            title="`❌`・Suspicion rejetée",
            description=f"Le mot **`{self.word}`** a été rejeté et ne sera plus suggéré.",
            color=embed_color(),
            footer=footer()
        )
        
        # Désactiver les boutons
        self.disabled = True
        view = View()
        for item in interaction.message.components[0].children:
            item.disabled = True
            view.add_item(item)
        
        await interaction.response.edit_message(embed=embed, view=view)


async def setup(bot):
    pass

