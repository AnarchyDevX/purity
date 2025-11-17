import discord
from functions.functions import *
from core import embedBuilder
from discord.ui import Button
from core.embedBuilder import embedBuilder

class disableSoutienButton(Button):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Désactivé",
            emoji="🔴"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        from views.soutien.enableButton import enableSoutienButton
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['soutien']['active'] = False
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        embed = embedBuilder(
            title="`🛠️`・Panel soutien",
            color=embed_color(),
            footer=footer(),
            fields={
                "`👘`・actif": (
                    "`oui`" if guildJSON['soutien']['active'] == True else "`non`",
                    True
                ),
                "`🪄`・status": (
                    f"`{guildJSON['soutien']['needed']}`",
                    True
                ),
                "`🛡️`・role ajouté": (
                    f"<@&{guildJSON['soutien']['role']}>" if guildJSON["soutien"]['role'] != None else "`non définit`",
                    True
                )
            }
        )
        view = discord.ui.View(timeout=None)
        view.add_item(enableSoutienButton(self.userId))
        view.add_item(disableSoutienButton(self.userId))
        await interaction.response.edit_message(embed=embed, view=view)