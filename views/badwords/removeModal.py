import discord
from discord.ui import TextInput, Modal
from functions.functions import *
from core.embedBuilder import embedBuilder

class badwordRemoveModal(Modal):
    def __init__(self, userId):
        self.userId = userId
        super().__init__(
            title="Retrait d'un badwords"
        )
        first = TextInput(
            label="Retrait du badword",
            style=discord.TextStyle.short,
            min_length=1,
            max_length=300,
            required=True,
            placeholder="Entrez votre badword ici..."
        )
        self.add_item(first)

    async def on_submit(self, interaction: discord.Interaction):
        from views.badwords.badwordAdd import badwordsAddButton
        from views.badwords.badwordRemove import badwordsRemoveButton
        mot = self.children[0].value
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        badwordsList = guildJSON['badwords']
        if mot not in badwordsList:
            return await err_embed(
                interaction,
                title="Badword non présent",
                description=f"Le mot `{mot}` n'est pas présent dans la liste des badwords."
            )
        badwordsList.remove(mot)
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        badwords = ", ".join(guildJSON['badwords'])
        embed: embedBuilder = embedBuilder(
            title="`🧪`・Badwords",
            description=(
                f"> `🪄`・**Total:** `{len(guildJSON['badwords'])}`\n"
                f"> `📜`・**Liste:** ```{badwords}```\n"
            ),
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(badwordsAddButton(self.userId))
        view.add_item(badwordsRemoveButton(self.userId))
        await interaction.response.edit_message(embed=embed, view=view)