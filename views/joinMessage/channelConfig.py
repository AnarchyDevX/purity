import asyncio
import discord
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder

class channelConfigButton(Button):
    def __init__(self, userId, bot):
        self.bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.grey,
            label="Channel", 
            emoji="🧪"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.joinMessage.disable import joinMessageDisable
        from views.joinMessage.enable import joinMessageEnable
        from views.joinMessage.embedEnable import EmbedEnableButton
        from views.joinMessage.embedDisable import EmbedDisableButton
        from views.joinMessage.messageConfig import MessageConfig

        def check(message):
            return message.author == interaction.user and len(message.channel_mentions) > 0
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")

        try: 
            await interaction.response.send_message("Merci d'envoyer le salon que vous voulez configurer.", ephemeral=True)
            message = await self.bot.wait_for("message", check=check, timeout=30)
            channel = message.channel_mentions[0]
            guildJSON['greeting']['channel'] = channel.id
            json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
            greeting = guildJSON["greeting"]
            embed = embedBuilder(
                title="`🖖`・Message de bienvenue",
                color=embed_color(),
                footer=footer(), 
                fields={
                    "`📍`・Actif": (
                        "`oui`" if greeting['active'] == True else "`non`", 
                        True
                    ),
                    "`🪼`・Type": (
                        "`message`" if greeting['type'] == "message" else "`embed`", 
                        True
                    ),
                    "`🪄`・Salon": (
                        f"<#{greeting['channel']}>" if greeting['channel'] != None else "`non définit`", 
                        True
                    ),
                    "`📢`・Mention": (
                        f"`non`" if greeting['mention'] == False else "`oui`", 
                        True
                    )
                }
            )
            view = discord.ui.View(timeout=None)
            view.add_item(joinMessageDisable(self.userId, self.bot) if greeting['active'] == True else joinMessageEnable(self.userId, self.bot))
            view.add_item(EmbedEnableButton(self.userId, self.bot) if greeting['type'] == "message" else EmbedDisableButton(self.userId, self.bot))
            view.add_item(channelConfigButton(self.userId, self.bot))
            view.add_item(MessageConfig(self.userId, self.bot))
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
            return await message.delete()

        except asyncio.TimeoutError:
            return await interaction.followup.send("Tu as mis trop de temps pour fournir le salon.", ephemeral=True)

        