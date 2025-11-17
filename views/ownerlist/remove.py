import discord
import asyncio
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class ownerRemoveButton(Button):
    def __init__(self, bot, userId):
        self.bot = bot
        self.userId = userId
        super().__init__(
            label="Retirer",
            style=discord.ButtonStyle.red,
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.ownerlist.add import ownerAddButton

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        ownerlist: list[int] = guildJSON['ownerlist']
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de fourni l'id du membre que vous voulez retirer de la liste des owners.", ephemeral=True)
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            member = message.content
            try:
                member = int(member)
            except ValueError:
                return await err_embed(
                    interaction=interaction,
                    title="Id invalide",
                    description=f"L'id du member que vous voulez retirer de la liste des owners est invalide",
                    followup=True
                )
            
            if member:
                if member in ownerlist:
                    ownerlist.remove(member)
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
                else:
                    await message.delete()
                    await err_embed(
                        interaction,
                        title="Ownerlist",
                        description=f"Le membre avec l'id `{member}` n'est pas dans la liste des owners.",
                        followup=True
                    )

        except asyncio.TimeoutError:
            return await interaction.followup.send("Vous avez dépasser le delai maximum.", ephemeral=True)
        