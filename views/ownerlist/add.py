import discord
import asyncio
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class ownerAddButton(Button):
    def __init__(self, bot, userId):
        self.bot = bot
        self.userId = userId
        super().__init__(
            label="Ajouter",
            style=discord.ButtonStyle.green,
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.ownerlist.remove import ownerRemoveButton

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        ownerlist: list[int] = guildJSON['ownerlist']
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de mentionner le membre que vous voulez ajouter dans la liste des owners.", ephemeral=True)
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            members: list[discord.Member] = message.mentions
            if members:
                for member in members:
                    if member.id not in ownerlist:
                        ownerlist.append(member.id)

                with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                    json.dump(guildJSON, f, indent=4)
                await message.delete()
                formatted = [f'<@{memberId}> `{memberId}`' for memberId in ownerlist]
                embed = embedBuilder(
                    title="`📜`・Liste des owners bot",
                    description='\n'.join(formatted),
                    color=embed_color(),
                    footer=footer()
                )
                view = View(timeout=None)
                view.add_item(ownerAddButton(self.bot, self.userId))
                view.add_item(ownerRemoveButton(self.bot, self.userId))
                await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)

        except asyncio.TimeoutError:
            return await interaction.followup.send("Vous avez dépasser le delai maximum.", ephemeral=True)
        