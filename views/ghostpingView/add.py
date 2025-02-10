import asyncio
import discord
from discord.ui import Button
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class addGhostPingButton(Button):
    def __init__(self, bot, userId):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Ajouter",
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            await unauthorized(interaction)

        from views.ghostpingView.remove import removeGhostPingButton

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        ghostpingList = guildJSON['ghostping']

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        await interaction.response.send_message("Merci de bien vouloir mentionner le salon a configurer", ephemeral=True)

        try:
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            channel = message.channel_mentions[0] if message.channel_mentions else None
            if channel:
                if channel.id in ghostpingList:
                    await message.delete()
                    return await interaction.followup.send(f"Le salon {channel.mention} est déjà un salon de ghostping a l'arrivée", ephemeral=True)
                
                ghostpingList.append(channel.id)
                json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w', encoding='utf-8'), indent=4)
                embed = embedBuilder(
                    title="`👻`・Ghostping",
                    description="\n".join(f'<#{channelId}> `{channelId}`' for channelId in ghostpingList),
                    color=embed_color(),
                    footer=footer()
                )
                view = discord.ui.View(timeout=None)
                view.add_item(addGhostPingButton(self.bot, self.userId))
                view.add_item(removeGhostPingButton(self.bot, self.userId))
                await message.delete()
                return await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
        
            else:
                await interaction.followup.send("Vous devez fournir un salon valide", ephemeral=True)
                await message.delete()

        except asyncio.TimeoutError:
            await interaction.followup.send("Vous avez dépasser le delais de réponse", ephemeral=True)
            await message.delete()
