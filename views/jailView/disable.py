import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class disableButtonJail(Button):
    def __init__(self, bot, userId):
        self.bot = bot
        self.userId = userId 
        super().__init__(
            style=discord.ButtonStyle.red,
            label="désactiver",
            emoji="🔴"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.jailView.enable import enableButtonView
        
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        guildJSON['jail']['active'] = False
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w', encoding='utf-8'), indent=4)
        embed = embedBuilder(
            title=f"`🔨`・Jail",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🟢`・Status": (
                    '`activé`' if guildJSON['jail']['active'] == True else '`désactivé`',
                    True
                ),
                "`👑`・Role prison": (
                    f"<@&{guildJSON['jail']['role']}>",
                    True
                )
            }
        )
        view = View(timeout=None)
        view.add_item(enableButtonView(self.userId, self.bot))
        return await interaction.response.edit_message(embed=embed, view=view)