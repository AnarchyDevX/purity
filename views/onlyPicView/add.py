import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class addButtonOnlypic(Button):
    def __init__(self, bot, userId):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Ajouté",
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.onlyPicView.remove import removeButtonOnlypic

        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        onlypicList = guildJSON['onlypic']

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de mentionner le salon que vous voulez configurer", ephemeral=True)
            message: discord.Message = await self.bot.wait_for('message', check=check, timeout=30.0)
            channel = message.channel_mentions[0] if message.channel_mentions else None
            if channel:
                if channel.id in onlypicList:
                    return await err_embed(
                        interaction,
                        title="Salon déja configurer",
                        description=f"Le salon {channel.mention} possède déjà le mode `onlypic` activé"
                    )
                else:
                    onlypicList.append(channel.id)
                    json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
                    onlypicList = [f"<#{channelId}> `{channelId}`" for channelId in guildJSON['onlypic']]
                    embed = embedBuilder(
                        title="`🥏`・Onlypic",
                        description="\n".join(onlypicList),
                        color=embed_color(),
                        footer=footer()
                    )
                    view = View(timeout=None)
                    view.add_item(addButtonOnlypic(self.bot, self.userId))
                    view.add_item(removeButtonOnlypic(self.bot, self.userId))
                    await interaction.followup.edit_message(embed=embed, view=view, message_id=interaction.message.id)
                    return await message.delete()
            else:
                await interaction.followup.send("Vous devez mentionner un salon valide", ephemeral=True)
                return await message.delete()
        except asyncio.TimeoutError:
            await message.delete()
            return await interaction.response.send_message("Vous avez dépasser le delais de réponse.", ephemeral=True)
