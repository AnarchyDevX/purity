import asyncio
import discord
from discord.ext import commands
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder

class removeGhostPingButton(Button):
    def __init__(self, bot, userId):
        self.bot: commands.Bot = bot    
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Supprimer",
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.ghostpingView.add import addGhostPingButton
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        ghostpingList = guildJSON["ghostping"]

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        await interaction.response.send_message("Merci de fournir l'id du salon que vous voulez retirer", ephemeral=True)

        try:
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            channelId = message.content
            try:
                channelId = int(channelId)
            except Exception:
                return await err_embed(
                    interaction,
                    title="Id manquant",
                    description=f"Je n'ai trouver aucun id valide dans votre message.",
                    followup=True
                )
            
            if channelId not in ghostpingList:
                return await interaction.followup.send("L'id du salon que vous avez fourni n'est pas dans la liste des salon ghostping", ephemeral=True)
            
            ghostpingList.remove(channelId)
            json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8'), indent=4)
            embed = embedBuilder(
                title="`👻`・Ghostping",
                description="\n".join(f'<#{channelId}> `{channelId}`' for channelId in ghostpingList),
                color=embed_color(),
                footer=footer()
            )
            view = discord.ui.View(timeout=None)
            view.add_item(addGhostPingButton(self.bot, self.userId))
            view.add_item(removeGhostPingButton(self.bot, self.userId))
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
            await message.delete()
        
        except asyncio.TimeoutError:
            await interaction.followup.send("Vous avez dépasser le delais de réponse", ephemeral=True)
            await message.delete()
