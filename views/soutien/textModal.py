import discord
import asyncio
from functions.functions import *
from discord.ui import Modal, TextInput

class textSoutienModal(Modal):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            title="Status du soutien"
        )
        first = TextInput(
            label="Status du soutien",
            style=discord.TextStyle.short,
            min_length=1,
            max_length=50,
            required=True,
            placeholder="Entrez le status requis ici..."
        )
        second = TextInput(
            label="Role ajouté",
            style=discord.TextStyle.short,
            min_length=1,
            max_length=50,
            required=True,
            placeholder="Entrez l'id du role..."
        )
        self.add_item(first)
        self.add_item(second)
    
    async def on_submit(self, interaction: discord.Interaction):
        from views.soutien.enableButton import enableSoutienButton
        from views.soutien.disableButton import disableSoutienButton
        try:
            roleId = int(self.children[1].value)
        except Exception:
            return await err_embed(
                interaction,
                title=f"Id Invalide",
                description="L'id que vous avez fourni est invalide. Merci de fournir un id correct.",
            )
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['soutien']['needed'] = self.children[0].value
        guildJSON['soutien']['role'] = roleId
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
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
