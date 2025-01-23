import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class EmbedEnableButton(Button):
    def __init__(self, userId, bot):
        self.bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Embed",
            emoji="⚙️"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.joinMessage.embedDisable import EmbedDisableButton
        from views.joinMessage.enable import joinMessageEnable
        from views.joinMessage.disable import joinMessageDisable
        from views.joinMessage.channelConfig import channelConfigButton
        from views.joinMessage.mentionEnable import MentionEnableButton
        from views.joinMessage.mentionDisable import MentionDisableButton

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['greeting']['type'] = "embed"
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
        view.add_item(EmbedDisableButton(self.userId, self.bot))
        view.add_item(channelConfigButton(self.userId, self.bot))
        view.add_item(MentionEnableButton(self.userId, self.bot) if greeting['mention'] == False else MentionDisableButton(self.userId, self.bot))

        return await interaction.response.edit_message(embed=embed, view=view)