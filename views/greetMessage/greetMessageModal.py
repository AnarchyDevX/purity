import discord
from discord.ui import Modal, TextInput
from functions.functions import *

class greetMessageModal(Modal):
    def __init__(self):
        super().__init__(
            title="Greet Message"
        )
        first = TextInput(
            label="Contenue du message d'arrivée",
            placeholder="Votre message ici...",
            style=discord.TextStyle.long,
            min_length=1,
            max_length=4000,
            required=True
        )
        self.add_item(first)
    
    async def on_submit(self, interaction: discord.Interaction):
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['greetmsg']["content"] = self.children[0].value
        guildJSON['greetmsg']['alive'] = True
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        await interaction.response.send_message("Le message a l'arrivée a été configuré avec succès", ephemeral=True)