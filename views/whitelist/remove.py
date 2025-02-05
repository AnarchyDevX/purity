import discord
import asyncio
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class whitelistRemoveButton(Button):
    def __init__(self, bot, userId):
        self.bot = bot
        self.userId = userId
        super().__init__(
            label="Retirer",
            style=discord.ButtonStyle.red,
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.whitelist.add import whitelistAddButton

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        whitelist: list[int] = guildJSON['whitelist']
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de fourni l'id du membre que vous voulez retirer de la whitelist.", ephemeral=True)
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            member = message.content
            try:
                member = int(member)
            except Exception as e:
                print(e)
                return await err_embed(
                    interaction=interaction,
                    title="Id invalide",
                    description=f"L'id du member que vous voulez retirer de la whitelist est invalide",
                    followup=True
                )
            
            if member:
                if member in whitelist:
                    whitelist.remove(member)
                    json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
                    await message.delete()
                    formatted = [f'<@{memberId}> `{memberId}`' for memberId in whitelist]
                    embed = embedBuilder(
                        title="`📜`・Whitelist",
                        description='\n'.join(formatted),
                        color=embed_color(),
                        footer=footer()
                    )
                    view = View(timeout=None)
                    view.add_item(whitelistAddButton(self.bot, self.userId))
                    view.add_item(whitelistRemoveButton(self.bot, self.userId))
                    await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
                else:
                    await message.delete()
                    await err_embed(
                        interaction,
                        title="Whitelist",
                        description=f"Le membre avec l'id `{member}` n'est pas dans la whitelist.",
                        followup=True
                    )

        except asyncio.TimeoutError:
            return await interaction.followup.send("Vous avez dépasser le delai maximum.", ephemeral=True)
        