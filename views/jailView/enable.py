import asyncio
import discord
from discord.ui import Button, View
from functions.functions import *
from core.embedBuilder import embedBuilder
from discord.ext import commands

class enableButtonView(Button):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Activer",
            emoji="🟢"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.jailView.disable import disableButtonJail

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
    
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de mentionner le role que vous voulez definir", ephemeral=True)
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            role = message.role_mentions[0] if message.role_mentions else None
            if role:
                guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
                guildJSON['jail']['active'] = True
                guildJSON['jail']['role'] = role.id
                json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8'), indent=4)
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
                            role.mention,
                            True
                        )
                    }
                )
                view = View(timeout=None)
                view.add_item(disableButtonJail(self.bot, self.userId))
                await interaction.followup.edit_message(embed=embed, view=view, message_id=interaction.message.id)
                return await message.delete()
            
        except asyncio.TimeoutError:
            pass