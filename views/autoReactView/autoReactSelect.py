import json
import discord
from discord.ui import Select
from discord import SelectOption
from functions.functions import *

class autoReactSelect(Select):
    def __init__(self, guild: discord.Guild, user: discord.User):
        self.guild: discord.Guild = guild
        self.user: discord.User = user
        self.config = load_json_file(f'./configs/{self.guild.id}.json')
        options = []
        reactConfig = self.config["configuration"]["autoreact"]
        for emojiId, data in reactConfig.items():
            emoji = discord.utils.get(self.guild.emojis, id=int(emojiId))
            content = data["content"]
            if emoji:
                options.append(
                    SelectOption(label=content, emoji=emoji, value=emojiId)
                )
                
        if reactConfig == {}:
            options = [SelectOption(label="Aucune configuration", value="no")]
            
        super().__init__(
            placeholder="Sélectionnez une réaction automatique",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await unauthorized(interaction)
            
        del self.config['configuration']['autoreact'][self.values[0]]
        with open(f'./configs/{interaction.guild.id}.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
        config2 = load_json_file(f"./configs/{self.guild.id}.json")
        
        view = None
        if config2["configuration"]["autoreact"] != {}:
            view = discord.ui.View(timeout=None)
            view.add_item(autoReactSelect(self.guild, self.user))
            
        await interaction.response.edit_message(view=view)
