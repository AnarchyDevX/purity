import asyncio
import discord
import json
from discord.ext import commands
from discord.ui import Button, Modal, TextInput
from functions.functions import *
from core.embedBuilder import embedBuilder

class ticketRoleRemoveModal(Modal):
    def __init__(self, userId, bot):
        self.userId = userId
        self.bot = bot
        super().__init__(title="Retirer un rôle de support")
        
        self.role_input = TextInput(
            label="ID du rôle à retirer",
            placeholder="Entrez l'ID du rôle",
            required=True,
            max_length=20
        )
        self.add_item(self.role_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        from views.ticketView.roleAdd import ticketRoleAddButton
        from views.ticketView.roleRemove import ticketRoleRemoveButton

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        try:
            role_id = int(self.role_input.value)
        except ValueError:
            return await err_embed(
                interaction,
                title="ID invalide",
                description="L'ID que vous avez fourni est invalide. Merci de fournir un ID correct."
            )
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        if 'tickets' not in guildJSON or 'roles' not in guildJSON['tickets']:
            return await err_embed(
                interaction,
                title="Aucun rôle configuré",
                description="Aucun rôle de support n'est configuré."
            )
        
        roleList = guildJSON['tickets']['roles']
        if role_id not in roleList:
            return await err_embed(
                interaction,
                title="Rôle non trouvé",
                description="Ce rôle n'est pas dans la liste des rôles de support."
            )
        
        roleList.remove(role_id)
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        
        rolesList = [f"<@&{roleId}> `{roleId}`" for roleId in guildJSON['tickets']['roles']]
        embed = embedBuilder(
            title="`🎫`・Liste des rôles de support",
            description='\n'.join(rolesList) if rolesList else "*Aucun rôle configuré*",
            footer=footer(),
            color=embed_color()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(ticketRoleAddButton(self.userId, self.bot))
        view.add_item(ticketRoleRemoveButton(self.userId, self.bot))
        await interaction.response.edit_message(embed=embed, view=view)

class ticketRoleRemoveButton(Button):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            label="Retirer",
            style=discord.ButtonStyle.red,
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):
        from views.ticketView.roleRemove import ticketRoleRemoveModal

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        await interaction.response.send_modal(ticketRoleRemoveModal(self.userId, self.bot))

