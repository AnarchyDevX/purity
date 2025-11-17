import discord
from discord.ext import commands
from functions.functions import *
from discord.ui import Modal, TextInput
from functions.functions import *

class autoRoleRemoveModal(Modal):
    def __init__(self, userId, bot):
        self.bot = bot
        self.userId = userId
        super().__init__(
            title="Retrait de l'autorole"
        )
        first = TextInput(
            label="Retrait du role",
            placeholder=f"Entrez l'id du role ici...",
            min_length=1,
            max_length=30,
            required=True,
            style=discord.TextStyle.short
        )
        self.add_item(first)

    async def on_submit(self, interaction: discord.Interaction):
        from views.autoRole.autoRoleAdd import autoroleAddButton
        from views.autoRole.autoRoleRemove import autoroleRemoveButton

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        roleList = guildJSON["configuration"]['autorole']
        try:
            roleId = int(self.children[0].value)
        except ValueError:
            return await err_embed(
                interaction,
                title=f"Role invalide",
                description=f"L'id du role que vous avez fourni est invalide"
            )
        if roleId not in roleList:
            return await err_embed(
                interaction,
                title="Rôle non configuré",
                description=f"Le role avec l'id que vous avez fourni n'est pas configuré pour l'autorole"
            )

        roleList.remove(roleId)
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        rolesList: list[str] = [f"<@&{roleId}>`{roleId}`" for roleId in guildJSON['configuration']['autorole']]
        embed: embedBuilder = embedBuilder(
            title="`✨`・Liste des roles ajoutés a l'arrivée",
            description='\n'.join(rolesList),
            footer=footer(),
            color=embed_color()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(autoroleAddButton(self.userId, self.bot))
        view.add_item(autoroleRemoveButton(self.userId, self.bot))
        await interaction.response.edit_message(embed=embed, view=view)