import discord
from functions.functions import *
from core import embedBuilder
from discord.ui import Button

class enableSoutienButton(Button):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Activé",
            emoji="🟢"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        from views.soutien.textModal import textSoutienModal
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['soutien']['active'] = True
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        await interaction.response.send_modal(textSoutienModal(self.userId))
