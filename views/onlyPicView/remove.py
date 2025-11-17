import asyncio
import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class removeButtonOnlypic(Button):
    def __init__(self, bot, userId):
        self.bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.red,
            label="Retirer",
            emoji="➖"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.onlyPicView.add import addButtonOnlypic

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        piclist = guildJSON['onlypic']

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de mentionner le salon que vous voulez configurer", ephemeral=True)
            message: discord.Message = await self.bot.wait_for('message', check=check, timeout=30.0)
            channelId = message.content
            try:
                channelId = int(channelId)
            except ValueError:
                return await err_embed(
                    interaction,
                    title="Id introuvable",
                    description=f"Je n'ai pas trouver d'id dans la reponse que vous m'avez fourni",
                    followup=True
                )
            if channelId not in piclist:
                return await err_embed(
                    interaction,
                    title="Id invalide",
                    description=f"L'id du salon que vous avez fourni n'est pas dans la liste des salon onlypics",
                    followup=True
                )
            
            piclist.remove(channelId)
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
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
            return await interaction.followup.edit_message(embed=embed, view=view, message_id=interaction.message.id)
        except asyncio.TimeoutError:
            return await interaction.response.send_message